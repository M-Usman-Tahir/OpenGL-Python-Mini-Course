import numpy as np
import pywavefront as pw
from math import radians

def getCubeVertices():
    return [[-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            # Back face
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5]]

def getCubeIndices():
    return [ # triangles as faces
    0, 1, 2, 2, 3, 0,  # Front face
    4, 5, 6, 6, 7, 4,  # Back face
    0, 3, 7, 7, 4, 0,  # Left face
    1, 2, 6, 6, 5, 1,  # Right face
    0, 1, 5, 5, 4, 0,  # Bottom face
    2, 3, 7, 7, 6, 2   # Top face
]

def getBulletVertices():
    return [[0,0,1],
            [-0.5,-0.5,2],
            [0.5,-0.5,2],
            [0.5,0.5,2],
            [-0.5,0.5,2]
            ]

def getBulletIndices():
    return [
    0, 1, 2, 
    0, 2, 3, 
    0, 3, 4, 
    0, 4, 1, 
    1, 2, 3,
    3, 4, 1
]

def getWoodColor():
    return np.array([[130, 84, 59]*36])/255

def getCubeFacesColors():
    return np.array([[255, 0, 0] *6,
            [0, 255, 0] *6,
            [0, 0, 255] *6,
            [255, 255, 0] *6,
            [255, 0, 255] *6,
            [0, 255, 255] *6])/255

def getTextureCords():
    return np.array([[0, 0], [1, 0], [1, 1], 
                     [1, 1], [0, 1], [0, 0]]*6)

def getCubeFaceNormals():
    return [[0.0, 0.0, 1.0] *6,
            [0.0, 0.0, -1.0] *6,
            [-1.0, 0.0, 0.0] *6,
            [1.0, 0.0, 0.0] *6,
            [0.0, -1.0, 0.0] *6,
            [0.0, 1.0, 0.0] *6]

def getCombinedVertices(vertices, indices, *args, Index=True):
    cubeVertices = np.array([vertices[i] for i in indices], dtype=np.float32) if Index else  vertices
    lenVert = len(cubeVertices)
    for ele in args:
        e = np.array(ele)
        cubeVertices = np.concatenate([cubeVertices, e.reshape(lenVert, e.size//lenVert)], axis=1, dtype=np.float32)
    return cubeVertices

def shiftObjectVertices(vertices, x=0, y=0, z=0, xpos=0, ypos=1, zpos=2):
    return np.array(list(map(lambda a: [ *a[:xpos], a[xpos] + x, a[ypos] + y, a[zpos] + z, *a[zpos+1:]], vertices)))

def ScaleObjectVertices(vertices, x=1, y=1, z=1, xpos=0, ypos=1, zpos=2):
    return np.array(list(map(lambda a: [ *a[:xpos], float(a[xpos]) * x, float(a[ypos]) * y, float(a[zpos]) * z, *a[zpos+1:]], vertices)))

def rotateObjectVertices(vertices, x=0, y=0, z=0, xpos=0, ypos=1, zpos=2, translated=[0,0,0]):
    vertices = shiftObjectVertices(vertices, *translated, xpos, ypos, zpos)
    x,y,z = radians(x), radians(y), radians(z)
    Rx = np.array([ [1,     0,          0],
                    [0, np.cos(x), -np.sin(x)],
                    [0, np.sin(x), np.cos(x)]])
    Ry = np.array([ [np.cos(y), 0, np.sin(y)],
                    [  0,       1,    0],
                    [-np.sin(y), 0, np.cos(y)]])
    Rz = np.array([ [np.cos(z), -np.sin(z), 0],
                    [np.sin(z), np.cos(z), 0],
                    [  0,       0,       1]])
    combined = np.array(np.dot(Rx, np.dot(Ry, Rz)))
    vertices = np.array(list(map(lambda a: [ *a[:xpos], *np.dot([a[xpos], a[ypos], a[zpos]], combined), *a[zpos+1:]], vertices)))
    return shiftObjectVertices(vertices, *list(map(lambda a: -a, translated)), xpos, ypos, zpos)

def getFloorTileVertices():
    return np.array([[0,0,0], [1,0,0], [1,0,1], [0,0,1]])

def getFloorTileIndices():
    return np.array([0,1,2,2,3,0])

def getObjectVertices(OBJname):
    objs = pw.Wavefront(OBJname, cache=True, parse=True)
    obj = objs.materials.popitem()[1]
    return np.array(obj.vertices, dtype=np.float32)

def getOBJVerticesOriented(name, shift, scale=0.01, rotation=[0,0,0]):
    V = np.array(getObjectVertices(name))
    V = V.reshape(V.size//8, 8)
    scaleObj = scale
    vertObj = ScaleObjectVertices(V, scaleObj, scaleObj, scaleObj, 5, 6, 7)
    vertObj = rotateObjectVertices(vertObj, *rotation, 5, 6, 7)
    vertObj = shiftObjectVertices(vertObj, *shift, 5, 6, 7)
    return vertObj

def createFloor(size):
    floorTileVertices = np.array(getCombinedVertices(getFloorTileVertices(), getFloorTileIndices(), [0, 1, 0]*6, [0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0], Index=True))
    floorVertices = floorTileVertices
    mid = size//2
    for i in range(size):
        for j in range(size):
            if i == j and j == mid:
                continue
            floorVertices = np.concatenate(
                [floorVertices, shiftObjectVertices(floorTileVertices, x=i-mid, z=j-mid)], axis=0)
    return shiftObjectVertices(floorVertices, y=-1)

def createMiniCam():
    miniCamViewVertices = np.array([[-0.98, -0.98, 0, 0],
                            [-0.4, -0.98, 1, 0],
                            [-0.4, -0.4, 1, 1],
                            [-0.4, -0.4, 1, 1],
                            [-0.98, -0.4, 0, 1],
                            [-0.98, -0.98, 0, 0]])

    return shiftObjectVertices(miniCamViewVertices, 0,1.38)
import numpy as np
import pywavefront as pw

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

def getFloorTileVertices():
    return np.array([[0,0,0], [1,0,0], [1,0,1], [0,0,1]])

def getFloorTileIndices():
    return np.array([0,1,2,2,3,0])

def getObjectVertices(OBJname):
    objs = pw.Wavefront(OBJname, cache=True, parse=True)
    obj = objs.materials.popitem()[1]
    return np.array(obj.vertices, dtype=np.float32)
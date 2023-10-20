import numpy as np

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

def getCombinedVertices(vertices, indices, *args):
    cubeVertices = np.array([vertices[i] for i in indices], dtype=np.float32)
    lenVert = len(cubeVertices)
    for ele in args:
        e = np.array(ele)
        cubeVertices = np.concatenate([cubeVertices, e.reshape(lenVert, e.size//lenVert)], axis=1, dtype=np.float32)
    return cubeVertices

def shiftObjectVertices(vertices, x=0, y=0, z=0):
    return np.array(list(map(lambda a: [a[0] + x, a[1] + y, a[2] + z, *a[3:]], vertices)))


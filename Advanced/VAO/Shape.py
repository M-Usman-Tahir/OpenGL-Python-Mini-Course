import numpy as np
from pyrr import Matrix44
from math import radians
from OpenGL.GL import *

class Shape:
    def __init__(self, vertices, material, shader, format=['3 0'], stride = 3, **kargs):
        self.kargs = kargs
        self.material = material
        self.vertices = np.array(vertices, dtype=np.float32)
        self.shader = shader
        self.transform = Matrix44.identity(dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        for i, ele in enumerate(format):
            vl = ele.split()
            glVertexAttribPointer(i, int(vl[0]), GL_FLOAT, GL_FALSE, stride*4, ctypes.c_void_p(int(vl[1])*4))
            glEnableVertexAttribArray(i)

    def getModelMatrix(self):
        self.transform = Matrix44.from_eulers([ 0 if not 'rotatex' in self.kargs else radians(self.kargs['rotatex']), 
                                                0 if not 'rotatey' in self.kargs else radians(self.kargs['rotatey']),
                                                0 if not 'rotatez' in self.kargs else radians(self.kargs['rotatez'])
                                                ], dtype=np.float32) @ self.transform
        self.transform = Matrix44.from_translation([0 if not 'translatex' in self.kargs else self.kargs['translatex'], 
                                                    0 if not 'translatey' in self.kargs else self.kargs['translatey'],
                                                    0 if not 'translatez' in self.kargs else self.kargs['translatez']
                                                    ], dtype=np.float32) @ self.transform
        self.transform = Matrix44.from_scale([  1 if not 'scalex' in self.kargs else self.kargs['scalex'], 
                                                1 if not 'scaley' in self.kargs else self.kargs['scaley'],
                                                1 if not 'scalez' in self.kargs else self.kargs['scalez']
                                                ], dtype=np.float32) @ self.transform
        return self.transform

    def destroy(self):
        self.shader.destroy()
        self.material.destroy()
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
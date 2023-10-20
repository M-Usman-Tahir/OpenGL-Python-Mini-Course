import numpy as np
import pygame as pg
from pyrr import Matrix44
from math import radians
from OpenGL.GL import *
from helpingFunctions import *

class Shape:
    def __init__(self, vertices, material, shader, FormatAlign = ['in_position'],format=['3 0'], stride = 3, **kargs):
        self.kargs = kargs
        self.material = material
        self.vertices = np.array(vertices, dtype=np.float32)
        self.shader = shader
        self.transform = Matrix44.identity(dtype=np.float32)
        self.speed = 0.01 if not 'speed' in self.kargs else self.kargs['speed']
        self.scalingFactor = 0.01 if not 'scalingFactor' in self.kargs else self.kargs['scalingFactor']

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        for i, ele in enumerate(format):
            vl = ele.split()
            pos = glGetAttribLocation(self.shader.shader_program, FormatAlign[i])
            glVertexAttribPointer(pos, int(vl[0]), GL_FLOAT, GL_FALSE, stride*4, ctypes.c_void_p(int(vl[1])*4))
            glEnableVertexAttribArray(pos)

    def getModelMatrix(self):
        self.rotate( 0 if not 'rotatex' in self.kargs else radians(self.kargs['rotatex']), 
                        0 if not 'rotatey' in self.kargs else radians(self.kargs['rotatey']),
                        0 if not 'rotatez' in self.kargs else radians(self.kargs['rotatez'])
                        )
        self.translate(0 if not 'translatex' in self.kargs else self.kargs['translatex'], 
                        0 if not 'translatey' in self.kargs else self.kargs['translatey'],
                        0 if not 'translatez' in self.kargs else self.kargs['translatez']
                        )
        self.scale(1 if not 'scalex' in self.kargs else self.kargs['scalex'], 
                    1 if not 'scaley' in self.kargs else self.kargs['scaley'],
                    1 if not 'scalez' in self.kargs else self.kargs['scalez']
                    )
        return self.transform

    def translate(self, x=0,y=0,z=0):
        self.transform = Matrix44.from_translation([x, y, z], dtype=np.float32) @ self.transform

    def rotate(self, x=0,y=0,z=0):
        self.transform = Matrix44.from_eulers([x, y, z], dtype=np.float32) @ self.transform

    def scale(self, x=1,y=1,z=1):
        self.transform = Matrix44.from_scale([x, y, z], dtype=np.float32) @ self.transform

    def move(self, keys):
        if 'move' in self.kargs and self.kargs['move']:
            if keys[pg.K_t]:
                self.translate(z=self.speed)
            if keys[pg.K_g]:
                self.translate(z=-self.speed)
            if keys[pg.K_f]:
                self.translate(x=self.speed)
            if keys[pg.K_h]:
                self.translate(x=-self.speed)
            if keys[pg.K_u]:
                self.scale(1+self.scalingFactor,1+self.scalingFactor,1+self.scalingFactor)
            if keys[pg.K_i]:
                self.scale(1-self.scalingFactor,1-self.scalingFactor,1-self.scalingFactor)


    def destroy(self):
        self.shader.destroy()
        self.material.destroy()
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
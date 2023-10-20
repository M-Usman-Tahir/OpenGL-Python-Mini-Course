import pygame as pg
from OpenGL.GL import *
import numpy as np
from math import radians
from pyrr import Matrix44
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer:
    def __init__(self, vertices, mode, n):
        self.mode = mode
        self.n = n
        # Initialize pygame
        self.display = (600, 600)
        pg.display.set_mode(self.display, pg.OPENGL | pg.DOUBLEBUF)
        # Initialize OpenGL
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Load and bind the texture
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        vertices = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # ^ Initialize Vertex Attribute Pointers
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 7*4, None)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 7*4, ctypes.c_void_p(2*4))
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 7*4, ctypes.c_void_p(5*4))

        # ^ Enable Vertex Attribute Pointers
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        # self.rotation = Matrix44.identity(dtype=np.float32)
        self.rotateAngle = radians(0.0)
        self.shader_program = self.compilerShader()
        # Get uniform locations
        self.rotation_location = glGetUniformLocation(self.shader_program, "rotate")
        # get uniform texture sampler location
        self.texture_sampler_location = glGetUniformLocation(self.shader_program, "texture_sampler")
        #  Load Texture
        self.loadTexture()

    def draw(self):
        self.rotate()
        
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)

    # Texture Loading
    def loadTexture(self): 
        # Load the texture image 
        texture_data = pg.image.load('t1.jpg')
        texture_surface = pg.transform.flip(texture_data, False, True)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        # Set texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0) 
        

    def compilerShader(self):
        with open("vertexShader2.txt", 'r') as vs: # ^ VertexShader
            vertex_shader_code = vs.read()
        with open("fragmentShader2.txt", 'r') as fs: # ^ FragmentShader
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram

    def rotate(self):
        self.rotateAngle += radians(0.1)
        rotationMatrix = Matrix44.from_eulers([self.rotateAngle, self.rotateAngle, self.rotateAngle], dtype='float32')
        glUniformMatrix4fv(self.rotation_location, 1, GL_FALSE, rotationMatrix)
    
    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteProgram(self.shader_program)
        glDeleteTextures(1, [self.texture_id]) 
        
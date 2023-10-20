import pygame as pg
from OpenGL.GL import *
import numpy as np
from math import radians
from pyrr import Matrix44
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT, GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT

class Renderer:
    def __init__(self, vertices, mode, n):

        self.mode = mode
        self.n = n

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Load and bind the texture
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        vertices = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        #  Initialize Vertex Attribute Pointers
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, None)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(2*4))
        #  Enable Vertex Attribute Pointers
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        self.rotateAngle = radians(0.0)
        self.scale = 1.0
        self.shader_program = self.compilerShader()

        # Get uniform locations
        self.rotation_location = glGetUniformLocation(self.shader_program, "rotate")
        # get uniform texture sampler location
        self.texture_sampler_location = glGetUniformLocation(self.shader_program, "texture_sampler")

        #  Load Texture
        self.loadTexture2()

    def draw(self):
        self.rotate()

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)

    # Texture Loading
    def loadTexture(self): 
        # Load the texture image 
        texture_data = pg.image.load('t2.png')
        texture_surface = pg.transform.flip(texture_data, False, False)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # Set texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0) 

    def loadTexture1(self):
        # Load the texture image
        texture_data = pg.image.load('t2.png')
        texture_surface = pg.transform.flip(texture_data, False, False)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        # glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) # ^ MipMap
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D) #^ gen Mip Map

        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0)

    def loadTexture2(self):
        self.check_anisotropic() # ^ check whether anistropic filter is supported or not
        # Load the texture image
        texture_data = pg.image.load('t4.png')
        texture_surface = pg.transform.flip(texture_data, False, False)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # ^ Enable anisotropic filtering (assuming you have checked for the extension)
        if self.max_anisotropy > 1.0: 
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, self.max_anisotropy)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0)

    def compilerShader(self):
        with open("vertexShader.txt", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.txt", 'r') as fs:
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram

    def rotate(self):
        self.rotateAngle = radians(85.0)
        # if self.scale >0.1:
        #     self.scale -= 0.001
        rotationMatrix = Matrix44.from_eulers([0.0, self.rotateAngle, 0.0], dtype='float32')
        # scaleMatrix = Matrix44.from_scale([self.scale, self.scale, 1.0], dtype='float32')
        glUniformMatrix4fv(self.rotation_location, 1, GL_FALSE, rotationMatrix)
    
    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteProgram(self.shader_program)
        #  texture Cleanup
        glDeleteTextures(1, [self.texture_id]) 
          
    def check_anisotropic(self):
        # Check for anisotropic filtering extension
        extension_count = glGetIntegerv(GL_NUM_EXTENSIONS)
        anisotropic_supported = False
        self.max_anisotropy = 1.0  # Default value

        for i in range(extension_count):
            extension = glGetStringi(GL_EXTENSIONS, i).decode('utf-8')
            if 'GL_EXT_texture_filter_anisotropic' in extension:
                anisotropic_supported = True
                # Retrieve the maximum anisotropy value
                self.max_anisotropy = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
                break

        if anisotropic_supported:
            print(f"Anisotropic Filtering Extension Supported. Maximum Anisotropy: {self.max_anisotropy}")
        else:
            print("Anisotropic Filtering Extension Not Supported. Using default values.")
            
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader 
import numpy as np
from math import radians
from pyrr import Matrix44
import glm

from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT, GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT
class CubeRenderer:
    def __init__(self, camera):
        self.camera = camera
        vertices = [
            # ^ Front face
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            # ^ Back face
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5]
        ]

        indices = [ #^ Squares as faces
            0, 1, 2, 3,  #^ Front face
            4, 5, 6, 7,  #^ Back face
            0, 3, 7, 4,  #^ Left face
            1, 2, 6, 5,  #^ Right face
            0, 1, 5, 4,  #^ Bottom face
            2, 3, 7, 6   #^ Top face
        ]

        tex_cords = [[0,0],
                     [1,0],
                     [1,1],
                     [0,1]
                  ]*6

        glEnable(GL_DEPTH_TEST)

        # ^ Create Vertices for all faces
        self.cubeVertices = np.array([vertices[i] for i in indices], dtype=np.float32)
        self.cubeVertices = np.concatenate([self.cubeVertices, np.array(tex_cords)], axis=1, dtype=np.float32)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.cubeVertices.nbytes, self.cubeVertices, GL_STATIC_DRAW)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        self.shader_program = self.compileShaderProgram()

        # ^ Vertex Attribute Pointer
        self.position = glGetAttribLocation(self.shader_program, "in_position")
        glVertexAttribPointer(self.position, 3, GL_FLOAT, GL_FALSE, 5*4, None)
        glEnableVertexAttribArray(self.position)
        # ^ Vertex Attribute Pointer
        self.tex = glGetAttribLocation(self.shader_program, "in_tex_cord")
        glVertexAttribPointer(self.tex, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(3*4))
        glEnableVertexAttribArray(self.tex)
        
        self.transfrom_loc = glGetUniformLocation(self.shader_program, "transform")
        self.texture_sampler_location = glGetUniformLocation(self.shader_program, "texture_sampler")
        
        self.rotation_matrix = np.identity(4, dtype=np.float32)
        self.rotateAnglex = radians(0)
        self.rotateAngley = radians(0)
        self.rotateAnglez = radians(0)
        self.loadTexture()


 # Texture Loading
    def loadTexture(self): 
        # Load the texture image 
        texture_data = pg.image.load('textures/t3.png')
        texture_surface = pg.transform.flip(texture_data, False, False)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)
        self.check_anisotropic()
        if self.max_anisotropy > 1.0: 
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, self.max_anisotropy)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # Set texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0) 

    def compileShaderProgram(self):
        with open("vertexShader.glsl", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.glsl", 'r') as fs:
            fragment_shader_code = fs.read()

        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram
    
    def draw(self):
        self.transform()
        # ^ Draw Squares through indices
        glDrawArrays(GL_QUADS, 0, len(self.cubeVertices))

    def get_view_projection(self): # ^ Getting View and Projection
        keys = pg.key.get_pressed()
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.camera.processInputs(keys, mouse_dx, mouse_dy)

        projection = self.camera.get_projection()
        # Set up the view transformation matrix (camera) using glm
        view = self.camera.get_view()

        # Combine the projection and view matrices
        return projection * view
    
    def transform(self):
        self.rotateAnglex = radians(75)
        self.rotateAngley = radians(0.1)
        self.rotateAnglez = radians(0.1)

        # ^ Model 
        rotationMatrix = Matrix44.from_eulers([self.rotateAnglex, self.rotateAngley, self.rotateAnglez], dtype='float32')
        
        MVP = self.get_view_projection() * rotationMatrix
        # ^ Pass the combined matrix to your shader program as needed
        glUniformMatrix4fv(self.transfrom_loc, 1, GL_FALSE, glm.value_ptr(MVP))

    def cleanup(self):

        glDeleteBuffers(1, [self.vbo])
        glDeleteProgram(self.shader_program)
        glDeleteTextures(1, [self.texture_id])
        glDisableVertexAttribArray(self.position)
        glDisableVertexAttribArray(self.tex)

         
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
            
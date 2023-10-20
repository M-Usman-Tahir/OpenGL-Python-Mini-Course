import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader 
import numpy as np
from math import radians
from pyrr import Matrix44
import glm
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT, GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT
 
class Renderer:
    def __init__(self, camera, light, mat, texture=None):
        self.light = light
        self.camera = camera
        self.mat = mat
        self.texture = texture
        
        # Create Vertices for all faces
        self.cubeVertices = np.array(self.mat.vertices, dtype=np.float32)
        print(self.cubeVertices)
        glEnable(GL_DEPTH_TEST)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.cubeVertices.nbytes, self.cubeVertices, GL_STATIC_DRAW)

        self.shader_program = self.compileShaderProgram()

        # Vertex Attribute Pointer
        self.position = glGetAttribLocation(self.shader_program, "in_position")
        glVertexAttribPointer(self.position, 3, GL_FLOAT, GL_FALSE, 9*4, None)
        glEnableVertexAttribArray(self.position)
       
        # Vertex Attribute Pointer
        self.color = glGetAttribLocation(self.shader_program, "in_color")
        glVertexAttribPointer(self.color, 2 if self.texture else 3, GL_FLOAT, GL_FALSE, 9*4, ctypes.c_void_p(3*4))
        glEnableVertexAttribArray(self.color)

        # Vertex Attribute Pointer
        self.normal = glGetAttribLocation(self.shader_program, "in_normal")
        glVertexAttribPointer(self.normal, 3, GL_FLOAT, GL_FALSE, 9*4, ctypes.c_void_p(6*4))
        glEnableVertexAttribArray(self.normal)

        self.VP_loc = glGetUniformLocation(self.shader_program, "VP")
        self.M_loc = glGetUniformLocation(self.shader_program, "M")
        self.ambient_loc = glGetUniformLocation(self.shader_program, "ambient")
        self.lightPos_loc = glGetUniformLocation(self.shader_program, "lightPos")
        self.lightInt_loc = glGetUniformLocation(self.shader_program, "lightInt")
        self.camPos_loc = glGetUniformLocation(self.shader_program, "camPos")
        self.specInt_loc = glGetUniformLocation(self.shader_program, "specInt")
        self.specR_loc = glGetUniformLocation(self.shader_program, "r_Spec")
        
        self.rotationMatrix = np.identity(4, dtype=np.float32)
        self.rotateAnglex = radians(0)
        self.rotateAngley = radians(0)
        self.rotateAnglez = radians(0)
        if self.texture:
            self.loadTexture()

    def compileShaderProgram(self):
        if self.texture:
            vs = "vertexShader2.glsl"
            fs = "fragmentShader2.glsl"
        else:
            vs = "vertexShader3.glsl"
            fs = "fragmentShader3.glsl"
        with open(vs, 'r') as vs:
            vertex_shader_code = vs.read()
        with open(fs, 'r') as fs:
            fragment_shader_code = fs.read()

        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram
      
    def draw(self):
        self.transform()
        glUniform3fv(self.ambient_loc, 1, self.mat.ambient)
        glUniform3fv(self.lightPos_loc, 1, self.light.pos)
        glUniform3fv(self.lightInt_loc, 1, self.mat.diffuse_intensity)
        glUniform3fv(self.camPos_loc, 1, self.camera.pos)
        glUniform3fv(self.specInt_loc, 1, self.mat.specular_shade)
        glUniform1i(self.specR_loc, self.mat.specRadius)
        
        glDrawArrays(GL_QUADS, 0, len(self.cubeVertices))


    def loadTexture(self): 
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        self.texture_sampler_location = glGetUniformLocation(self.shader_program, "tex_sampler")

        texture_data = pg.image.load(self.texture)
        texture_surface = pg.transform.flip(texture_data, False, False)  # Correct texture orientation
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # Set texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        # Bind the texture before rendering
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_location, 0) 

    def get_view_projection(self): # Getting View and Projection
        keys = pg.key.get_pressed()
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.camera.processInputs(keys, mouse_dx, mouse_dy)

        projection = self.camera.get_projection()
        view = self.camera.get_view()
        return projection * view
    
    def transform(self):
        self.rotateAnglex -= radians(0.1)
        self.rotateAngley = radians(0.1)
        self.rotateAnglez -= radians(0.1)
        #  Model
        self.rotationMatrix = Matrix44.from_eulers([self.rotateAnglex, self.rotateAngley,self.rotateAnglez], dtype=np.float32)

        VP = self.get_view_projection() 
        #  Pass the combined matrix to your shader program as needed
        glUniformMatrix4fv(self.VP_loc, 1, GL_FALSE, glm.value_ptr(VP))
        glUniformMatrix4fv(self.M_loc, 1, GL_FALSE, self.rotationMatrix)
        
    def destroy(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteProgram(self.shader_program)
        glDisableVertexAttribArray(self.position)
        glDisableVertexAttribArray(self.color)
        glDisableVertexAttribArray(self.normal)
        glDeleteTextures(1, [self.texture_id]) if self.texture else 0
    
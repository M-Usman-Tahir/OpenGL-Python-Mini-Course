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

        vertices = np.array(vertices, dtype=np.float32)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, None)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(2*4))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        # Create MVP matrices
        self.model_matrix = Matrix44.identity(dtype=np.float32)
        self.view_matrix = Matrix44.identity(dtype=np.float32)
        self.projection_matrix = Matrix44.identity(dtype=np.float32)

        # Compile shaders
        self.shader_program = self.compilerShader()

        # Get uniform locations
        self.model_matrix_location = glGetUniformLocation(self.shader_program, "model_matrix")
        self.view_matrix_location = glGetUniformLocation(self.shader_program, "view_matrix")
        self.projection_matrix_location = glGetUniformLocation(self.shader_program, "projection_matrix")

    def draw(self):
        self.update_mvp_matrices()

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)

    def compilerShader(self):
        with open("vertexShader3.txt", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.txt", 'r') as fs:
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram

    def update_mvp_matrices(self):
        fov = 45.0 #* degrees
        aspect = 1.0
        near = 0.1
        far = 10.0
        
        camera_position = [0.0, 0.0, -3.0]
        view_rotation = radians(1.0)
        
        camera_transformation = Matrix44.from_translation(camera_position, dtype=np.float32)
        view_transformation =  Matrix44.from_eulers([0.0, 0.0, view_rotation], dtype=np.float32) 

        self.model_matrix = Matrix44.from_translation([0.5, 0.0, 0.0],dtype=np.float32) 
        self.view_matrix = (camera_transformation * view_transformation) 
        self.projection_matrix = Matrix44.perspective_projection(fov, aspect, near, far, dtype=np.float32)
        glUniformMatrix4fv(self.model_matrix_location, 1, GL_FALSE, self.model_matrix)
        glUniformMatrix4fv(self.view_matrix_location, 1, GL_FALSE, self.view_matrix)
        glUniformMatrix4fv(self.projection_matrix_location, 1, GL_FALSE, self.projection_matrix)

    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteProgram(self.shader_program)
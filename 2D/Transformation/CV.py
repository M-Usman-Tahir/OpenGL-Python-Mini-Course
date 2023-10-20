import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import radians
from pyrr import Matrix44

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

        # Set up initial camera position
        degrees1 = 30.0
        degrees2 = 10.0
        degrees3 = 0.0
        self.camera_position = [-0.2, -0.2, 0.0]
        self.view_rotation = [radians(degrees1), radians(degrees2), radians(degrees3)]

        # Compile shaders
        self.shader_program = self.compilerShader()

        # Get uniform locations
        self.view_matrix_location = glGetUniformLocation(self.shader_program, "view_matrix")

    def draw(self):
        self.update_matrices()

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)

    def compilerShader(self):
        with open("vertexShader4.txt", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.txt", 'r') as fs:
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram

    def update_matrices(self):
        camera_matrix =  Matrix44.from_translation(self.camera_position, dtype=np.float32)
        View_matrix = Matrix44.from_eulers(self.view_rotation,dtype=np.float32)
        self.view_matrix = camera_matrix * View_matrix

        glUniformMatrix4fv(self.view_matrix_location, 1, GL_FALSE, self.view_matrix)

    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteProgram(self.shader_program)
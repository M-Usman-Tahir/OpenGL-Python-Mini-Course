import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader 
import numpy as np
from math import radians
from pyrr import Matrix44
import glm

class CubeRenderer:
    def __init__(self, camera):
        self.camera = camera
        self.vertices = np.array([
            # Vertex positions      # ^ Vertex colors
            [-0.5, -0.5, 0.5,       1.0, 0.0, 0.0],  
            [0.5, -0.5, 0.5,        0.0, 1.0, 0.0],  
            [0.5, 0.5, 0.5,         0.0, 0.0, 1.0],  
            [-0.5, 0.5, 0.5,        1.0, 1.0, 0.0],  
            #  Back face
            [-0.5, -0.5, -0.5,      1.0, 0.0, 1.0],
            [0.5, -0.5, -0.5,      0.0, 1.0, 1.0],
            [0.5, 0.5, -0.5,      1.0, 1.0, 1.0],
            [-0.5, 0.5, -0.5,      0.0, 0.0, 0.0]
        ], dtype=np.float32)

        self.indices = np.array([ # triangles as faces
            0, 1, 2, 2, 3, 0,  # Front face
            4, 5, 6, 6, 7, 4,  # Back face
            0, 3, 7, 7, 4, 0,  # Left face
            1, 2, 6, 6, 5, 1,  # Right face
            0, 1, 5, 5, 4, 0,  # Bottom face
            2, 3, 7, 7, 6, 2   # Top face
        ], dtype=np.uint32)

        glEnable(GL_DEPTH_TEST)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Element buffer object
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.shader_program = self.compileShaderProgram()

        # After setting up the position attribute
        self.position = glGetAttribLocation(self.shader_program, "in_position")
        glVertexAttribPointer(self.position, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)
        glEnableVertexAttribArray(self.position)

        # ^ Add a new attribute for colors
        self.color = glGetAttribLocation(self.shader_program, "in_color")
        glVertexAttribPointer(self.color, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(self.color)

        self.transfrom_loc = glGetUniformLocation(self.shader_program, "transform")
        
        self.rotation_matrix = np.identity(4, dtype=np.float32)
        self.rotateAnglex = radians(0)
        self.rotateAngley = radians(0)
        self.rotateAnglez = radians(0)

    def compileShaderProgram(self):
        with open("vert2.glsl", 'r') as vs:
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
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def get_view_projection(self):
        keys = pg.key.get_pressed()
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.camera.processInputs(keys, mouse_dx, mouse_dy)

        projection = self.camera.get_projection()
        # Set up the view transformation matrix (camera) using glm
        view = self.camera.get_view()

        # Combine the projection and view matrices
        return projection * view
    
    def transform(self):
        self.rotateAnglex += radians(0.5)
        self.rotateAngley += radians(0.1)
        self.rotateAnglez += radians(0.1)

        rotationMatrix = Matrix44.from_eulers([self.rotateAnglex, self.rotateAngley, self.rotateAnglez], dtype='float32')
        
        MVP = self.get_view_projection() * rotationMatrix
        # Pass the combined matrix to your shader program as needed
        glUniformMatrix4fv(self.transfrom_loc, 1, GL_FALSE, glm.value_ptr(MVP))

    def cleanup(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteBuffers(1, [self.ebo])
        glDeleteProgram(self.shader_program)
    
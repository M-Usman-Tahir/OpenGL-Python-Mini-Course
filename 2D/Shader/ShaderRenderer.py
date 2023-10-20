from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

class Renderer:
    def __init__(self, cord, mode, n):
        self.mode =mode
        self.n = n
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        cords = np.array(cord, dtype=np.float32)
        
        glBufferData(GL_ARRAY_BUFFER, cords.nbytes, cords, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, None)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(2*4))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        self.compilerShader()

    def compilerShader(self):
        with open("vertexShader.txt", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.txt", 'r') as fs:
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)

    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)


    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])

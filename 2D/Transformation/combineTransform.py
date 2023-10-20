from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
from pyrr import Matrix44

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

        self.shaderProgram = self.compilerShader()
        self.r = 0.0
        self.s = 1.0
        self.t = 0.0
        self.rotation_location = glGetUniformLocation(self.shaderProgram, "rotate")
        self.scale_location = glGetUniformLocation(self.shaderProgram, "scale")
        self.translate_location = glGetUniformLocation(self.shaderProgram, "translate")

        self.R_identity = Matrix44.identity(dtype='float32')
        self.S_identity = Matrix44.identity(dtype='float32')
        self.T_identity = Matrix44.identity(dtype='float32')
    
    def transform(self):
        self.r += 0.01
        self.s += 0.001
        self.t += 0.0005
        rotationMatrix = Matrix44.from_eulers([self.r, 0.0, 0.0], dtype='float32') @ self.R_identity
        scaleMatrix = Matrix44.from_scale([self.s, 1.0, 1.0], dtype='float32') @ self.S_identity
        translateMatrix = Matrix44.from_translation([self.t, 0.0, 0.0], dtype='float32') @ self.T_identity
        glUniformMatrix4fv(self.rotation_location, 1, GL_FALSE, rotationMatrix)
        glUniformMatrix4fv(self.scale_location, 1, GL_FALSE, scaleMatrix)
        glUniformMatrix4fv(self.translate_location, 1, GL_FALSE, translateMatrix)

    def compilerShader(self):
        with open("vertexShader2.txt", 'r') as vs:
            vertex_shader_code = vs.read()
        with open("fragmentShader.txt", 'r') as fs:
            fragment_shader_code = fs.read()
        vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shaderProgram = compileProgram(vertexShader, fragmentShader)

        glUseProgram(shaderProgram)
        return shaderProgram

    def draw(self):
        self.transform()
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(self.mode, 0, self.n)


    def cleanup(self):
        glDeleteBuffers(1, [self.VBO])

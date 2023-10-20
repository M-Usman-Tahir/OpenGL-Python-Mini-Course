from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Shader:
    def __init__(self, vertexShader, fragmentShader):

        with open(vertexShader, 'r') as vs:
            vertex_shader_code = vs.read()
        with open(fragmentShader, 'r') as fs:
            fragment_shader_code = fs.read()

        self.__vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        self.__fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        self.shader_program = compileProgram(self.__vertexShader, self.__fragmentShader)

        self.VP_loc = glGetUniformLocation(self.shader_program, "VP")
        self.M_loc = glGetUniformLocation(self.shader_program, "M")
        self.ambient_loc = glGetUniformLocation(self.shader_program, "ambient")
        self.lightPos_loc = glGetUniformLocation(self.shader_program, "lightPos")
        self.lightInt_loc = glGetUniformLocation(self.shader_program, "lightInt")
        self.diffuseInt_loc = glGetUniformLocation(self.shader_program, "diffuseInt")
        self.camPos_loc = glGetUniformLocation(self.shader_program, "camPos")
        self.specInt_loc = glGetUniformLocation(self.shader_program, "specInt")
        self.texture_sampler_location = glGetUniformLocation(self.shader_program, "tex_sampler")
    
    def destroy(self):
        try:
            glDeleteProgram(self.shader_program)
        except: ...
            
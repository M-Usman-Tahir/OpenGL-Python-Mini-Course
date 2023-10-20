from OpenGL.GL import *
import pygame as pg
import glm

class Renderer:
    def __init__(self, shapes, camera, light) -> None:
        self.shapes = shapes
        self.camera = camera
        self.light = light
        [shape.material.LightenUp(self.light.color) for shape in self.shapes]

    def render(self):
        for shape in self.shapes:
            glBindVertexArray(shape.vao)
            glUseProgram(shape.shader.shader_program)
            self.Update_MVP(shape)
            self.loadLights(shape)
            if shape.material.texture:
                self.loadTexture(shape)
            glDrawArrays(GL_TRIANGLES, 0, len(shape.vertices))
            glBindVertexArray(0)

    def Update_MVP(self, shape):
        keys = pg.key.get_pressed()
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.camera.processInputs(keys, mouse_dx, mouse_dy)

        model = shape.getModelMatrix()
        view = self.camera.get_view()
        projection = self.camera.get_projection()
        VP = projection * view
        glUniformMatrix4fv(shape.shader.VP_loc, 1, GL_FALSE, glm.value_ptr(VP))
        glUniformMatrix4fv(shape.shader.M_loc, 1, GL_FALSE, model)
    
    def loadLights(self, shape):
        glUniform3fv(shape.shader.ambient_loc, 1, shape.material.ambient)
        glUniform3fv(shape.shader.diffuseInt_loc, 1, shape.material.diffuse_intensity)
        glUniform3fv(shape.shader.specInt_loc, 1, shape.material.specular_shade)
        glUniform3fv(shape.shader.lightPos_loc, 1, self.light.pos)
        glUniform3fv(shape.shader.lightInt_loc, 1, self.light.intensity)
        glUniform3fv(shape.shader.camPos_loc, 1, self.camera.pos)
    
    def loadTexture(self, shape):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, shape.material.texture.texture_id)
        glUniform1i(shape.shader.texture_sampler_location, 0) 
    
    def destroy(self):
        for shape in self.shapes:
            shape.destroy()

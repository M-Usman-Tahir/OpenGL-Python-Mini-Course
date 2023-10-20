from OpenGL.GL import *
import pygame as pg
import glm

class Renderer:
    def __init__(self, shapes, camera, light, fbo=None, fboScreen=None, staticCamera=None) -> None:
        self.shapes = shapes
        self.camera = camera
        self.staticCamera = staticCamera
        self.light = light
        self.fbo = fbo
        self.fboScreen = fboScreen
        [shape.material.LightenUp(self.light.color) for shape in self.shapes]

    def draw(self, shape, static=False):
        glUseProgram(shape.shader.shader_program)
        glBindVertexArray(shape.vao)
        self.Update_MVP(shape, static)
        self.loadLights(shape)
        if shape.material.texture:
            self.loadTexture(shape)
        glDrawArrays(GL_TRIANGLES, 0, len(shape.vertices))
        glBindVertexArray(0)

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for shape in self.shapes:
            self.draw(shape)
        if self.fbo:
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo.fbo)
            glClearColor(0.1, 0.1, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for shape in self.shapes:
                self.draw(shape, True)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glUseProgram(self.fboScreen.shader.shader_program)
            glBindVertexArray(self.fboScreen.vao)
            glBindTexture(GL_TEXTURE_2D, self.fboScreen.material.texture.texture_id)
            self.Update_MVP(self.fboScreen, True)
            glDrawArrays(GL_TRIANGLES, 0, len(self.fboScreen.vertices))
            glBindVertexArray(0)


    def Update_MVP(self, shape, static=False):
        if static:
            view = self.staticCamera.get_view()
            projection = self.staticCamera.get_projection()
        else:
            keys = pg.key.get_pressed()
            mouse_dx, mouse_dy = pg.mouse.get_rel()
            self.camera.processInputs(keys, mouse_dx, mouse_dy)
            view = self.camera.get_view()
            projection = self.camera.get_projection()
            shape.move(keys)

        VP = projection * view
        model = shape.getModelMatrix()
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
        if self.fbo:
            self.fbo.destroy()

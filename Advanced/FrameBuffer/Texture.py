import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT, GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT

class Texture:
    def __init__(self, image=None, width=500, height=500) -> None:
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        if image:
            texture_data = pg.image.load(image)
            texture_surface = pg.transform.flip(texture_data, False, False)
            self.width, self.height = texture_surface.get_width(), texture_surface.get_height()
            texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))
        else:
            texture_data = None
            print("Empty texture generated...")
            self.width, self.height = width, height

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        if image:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        if image:
            glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

    def destroy(self):
        try:
            glDeleteTextures(1, [self.texture_id])
        except: ...
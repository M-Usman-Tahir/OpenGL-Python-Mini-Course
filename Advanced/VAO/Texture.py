import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT, GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT

class Texture:
    def __init__(self, image) -> None:
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        texture_data = pg.image.load(image)
        texture_surface = pg.transform.flip(texture_data, False, False)
        texture_data = pg.image.tostring(texture_surface, 'RGBA', 1)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def destroy(self):
        try:
            glDeleteTextures(1, [self.texture_id])
        except: ...
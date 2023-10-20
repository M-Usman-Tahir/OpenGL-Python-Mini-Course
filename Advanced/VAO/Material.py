import numpy as np

class Material:
    def __init__(self, ambient = 0.2, diffuse_intensity = 0.6, specular_shade = 2.0, Type=None, Texture=None):
        self.texture = Texture
        self.__amb = ambient
        self.__diff = diffuse_intensity
        self.__spec = specular_shade
        self.Type = Type
        self.ambient = [0,0,0]
        self.diffuse_intensity = [0,0,0]
        self.specular_shade = [0,0,0]

    def LightenUp(self, color):
        match self.Type:
            case 'dull':
                self.dull(color)
            case 'bright':
                self.bright(color)
            case 'metallic':
                self.metallic(color)
            case 'dark':
                self.dark(color)
            case 'oily':
                self.oily(color)
            case 'iluminous':
                self.iluminous(color)
            case _:
                self.ambient = self.__amb * color
                self.diffuse_intensity = self.__diff * color
                self.specular_shade = self.__spec * color

    def dull(self, color):
        self.ambient = 0.2 * color
        self.diffuse_intensity = 0.5 * color
        self.specular_shade = 0 * color

    def bright(self, color):
        self.ambient = 0.2 * color
        self.diffuse_intensity = 0.8 * color
        self.specular_shade = 0 * color

    def metallic(self, color):
        self.ambient = 0.2 * color
        self.diffuse_intensity = 0.6 * color
        self.specular_shade = 2 * color

    def dark(self, color):
        self.ambient = 0.2 * color
        self.diffuse_intensity = 0 * color
        self.specular_shade = 0 * color
  
    def oily(self, color):
        self.ambient = 0.2 * color
        self.diffuse_intensity = 0.4 * color
        self.specular_shade = 2 * color

    def iluminous(self, color):
        self.ambient = 0.8 * color
        self.diffuse_intensity = 0 * color
        self.specular_shade = 0 * color
    
    def destroy(self):
        if self.texture:
            self.texture.destroy()
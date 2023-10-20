import numpy as np
class Material:
    def __init__(self, vertices, ambient = 0.2, diffuse_intensity = 0.6, specular_shade = 2.0, specRadius = 5, color = [1,1,1]):
        self.vertices = vertices
        COLOR = np.array(color)
        self.ambient = ambient * COLOR
        self.diffuse_intensity = diffuse_intensity * COLOR
        self.specular_shade = specular_shade * COLOR
        self.specRadius = int(2**specRadius)
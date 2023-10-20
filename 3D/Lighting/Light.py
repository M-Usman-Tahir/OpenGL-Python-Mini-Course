import numpy as np

class Light:
    def __init__(self, pos = [0, 0, 4], color = [1,1,1], ambient = 0.2, diffuse_intensity = 0.6, specular_shade = 2.0):
        self.pos = np.array(pos, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.ambient = ambient * self.color
        self.diffuse_intensity = diffuse_intensity * self.color
        self.specular_shade = specular_shade * self.color
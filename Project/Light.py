import numpy as np

class Light:
    def __init__(self, pos = [0, 4, 8], color = [1,1,1], intensity = [1,1,1]):
        self.pos = np.array(pos, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.intensity = np.array(intensity, dtype=np.float32)
        
import pygame as pg
import numpy as np
from OpenGL.GL import *
import glm

class Camera:
    def __init__(self, width, height, initialPos = [0.0, 0.0, 4.0], initialFront = [0.0, 0.0, -2.0], initialUp = [0.0, 1.0, 0.0]):
        self.width = width
        self.height = height
        self.pos = np.array(initialPos, dtype=np.float32) 
        self.front = np.array(initialFront, dtype=np.float32) 
        self.up = np.array(initialUp, dtype=np.float32)
        
        self.scrollspeed = 0.1  
        self.speed = 0.005  
        self.pitch = 0.0
        self.yaw = -90.0
        self.mouse_sensitivity = 0.01

    def get_projection(self):
        return glm.perspective(glm.radians(45.0), (self.width / self.height), 0.1, 100.0)

    def get_view(self):
        return glm.lookAt(glm.vec3(*self.pos), glm.vec3(*(self.pos + self.front)), glm.vec3(*self.up))
    
    def zoom(self, z):
        self.pos += self.scrollspeed * self.front * z
    
    def processInputs(self, keys, mouse_dx, mouse_dy):
        if keys[pg.K_w]:
            self.pos += self.up * self.speed
        if keys[pg.K_s]:
            self.pos -= self.up * self.speed 
        if keys[pg.K_q]:
            self.pos += self.speed * self.front
        if keys[pg.K_e]:
            self.pos -= self.speed * self.front
        if keys[pg.K_a]:
            self.pos -= np.cross(self.front, self.up) * self.speed
        if keys[pg.K_d]:
            self.pos += np.cross(self.front, self.up) * self.speed

        self.yaw += mouse_dx * self.mouse_sensitivity
        self.pitch += mouse_dy * self.mouse_sensitivity

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.front = direction / np.linalg.norm(direction)

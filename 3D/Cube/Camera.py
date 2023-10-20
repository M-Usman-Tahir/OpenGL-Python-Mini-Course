import pygame as pg
import numpy as np
from OpenGL.GL import *
import glm

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = np.array([0.0, 0.0, 3.0], dtype=np.float32) # at z = 3
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32) # looking towards negative z axis
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32) # setting up direction
        
        self.scrollspeed = 0.05  # Adjust this for movement speed via mouse scroll
        self.speed = 0.005  # Adjust this for movement speed via buttons
        self.pitch = 0.0
        self.yaw = -90.0
        self.mouse_sensitivity = 0.01

    def get_projection(self):
        return glm.perspective(glm.radians(45.0), (self.width / self.height), 0.1, 100.0)

    def get_view(self):
        return glm.lookAt(glm.vec3(*self.pos), glm.vec3(*(self.pos + self.front)), glm.vec3(*self.up))
    
    def zoom(self, z):
        self.pos[2] += z * self.scrollspeed
    
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
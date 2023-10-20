import pygame as pg
from OpenGL.GL import *
import numpy as np

class triangleRenderer:
    def __init__(self):
        # initialize pygame
        self.display = (600, 600)
        pg.display.set_mode(self.display, pg.OPENGL| pg.DOUBLEBUF)
        # initilize OpenGL
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.triangle_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.triangle_VBO)

        triangle_cords = np.array([
            (0.0, 0.5),
            (-0.5, -0.5),
            (0.5, -0.5)
        ], dtype=np.float32)

        glBufferData(GL_ARRAY_BUFFER, triangle_cords.nbytes, triangle_cords, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.triangle_VBO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def cleanup(self):
        glDeleteBuffers(1, [self.triangle_VBO])

    def render(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.cleanup()
                    pg.quit()
            glClear(GL_COLOR_BUFFER_BIT)
            glColor3f(1.0, 1.0, 0)
            self.draw()
            pg.display.flip()

if __name__ == "__main__":
    triangle = triangleRenderer()
    triangle.render()
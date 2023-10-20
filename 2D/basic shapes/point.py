import pygame as pg
from OpenGL.GL import *
import numpy as np

class PointRenderer:
    def __init__(self):
        # initialize pygame
        self.display = (600, 600)
        pg.display.set_mode(self.display, pg.OPENGL| pg.DOUBLEBUF)
        # initilize OpenGL
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glPointSize(5.0)
        # Create VBO for point
        self.point_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.point_VBO)
        # define coordinates for point
        point_cord = np.array([0.0, 0.0], dtype=np.float32)
        # Upload data to Buffer
        glBufferData(GL_ARRAY_BUFFER, point_cord.nbytes, point_cord, GL_STATIC_DRAW)
        #Specify the vertex attribute pointer
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def drawPoint(self):
        # bind the VBO with buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.point_VBO)
        glDrawArrays(GL_POINTS, 0, 1)

    def cleanup(self):
        glDeleteBuffers(1, [self.point_VBO])

    def render(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.cleanup()
                    pg.quit()
            glClear(GL_COLOR_BUFFER_BIT)
            glColor3f(1.0, 1.0, 0)
            self.drawPoint()
            pg.display.flip()

if __name__ == "__main__":
    point = PointRenderer()
    point.render()
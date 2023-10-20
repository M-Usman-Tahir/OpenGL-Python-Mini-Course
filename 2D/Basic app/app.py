import pygame as pg
from OpenGL.GL import *

class BasicWindow:
    def __init__(self):
        #initilize PYGAME
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        # initilize OPEN-GL
        glClearColor(0,1,0,0.2)
        # Startup
        self.startup()
    
    def startup(self):

        while True:
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    self.end()

            # refresh the screen
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            self.clock.tick()

    def end(self):
        pg.quit()

if __name__ == "__main__":
    app = BasicWindow()
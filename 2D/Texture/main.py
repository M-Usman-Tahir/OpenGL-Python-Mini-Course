from OpenGL.GL import *

from Texture import Renderer

import pygame as pg
def main():
    pg.init()

    # ^ Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)  # Enable multisampling
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)  # Set the number of samples

    pg.display.set_mode((600, 600), pg.OPENGL | pg.DOUBLEBUF)

    glClearColor(0.2, 0.2, 0.2, 0.0)
    # x, y, #^ t_x, t_y
    Triangle = Renderer([-0.5, -0.5, 0.0, 0.0,
                        0.5, -0.5, 1.0, 0.0,
                        0.5, 0.5, 1.0, 1.0,
                        -0.5, 0.5, 0.0, 1.0
                        ], GL_QUADS, 4)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Triangle.cleanup()
                pg.quit()
                quit()
        
        glClear(GL_COLOR_BUFFER_BIT)
        Triangle.draw()
        pg.display.flip()

if __name__ == "__main__":
    main()
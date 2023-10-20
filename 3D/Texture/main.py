import pygame as pg
from OpenGL.GL import *

from CubeTexture import CubeRenderer
from Camera import Camera

def main():
    pg.init()
    
    # Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)  # Enable multisampling
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)  # Set the number of samples

    display = (800, 600)
    pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    camera = Camera(*display)
    cube = CubeRenderer(camera)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                cube.cleanup()
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    camera.zoom(1)
                elif event.button == 5:  # Scroll down
                    camera.zoom(-1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube.draw()
        pg.display.flip()

if __name__ == "__main__":
    main()

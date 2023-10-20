import pygame as pg
from GameEngine import GameEngine
from OpenGL.GL import *


def main():
    pg.init()

    # # Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)

    display = (800, 600)
    pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    pg.event.set_grab(True)
    pg.mouse.set_visible(False)

    Game = GameEngine(display)
    Game.start()

if __name__ == "__main__":
    main()

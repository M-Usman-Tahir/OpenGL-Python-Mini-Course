import numpy as np
import pygame as pg
from Camera import Camera
from helpingFunctions import *
from Light import Light
from Material import Material
from OpenGL.GL import *
from Renderer import Renderer
from Shader import Shader
from Shape import Shape
from Texture import Texture

vertices_normal_cube_colored = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getCubeFaceNormals(), getCubeFacesColors()))
vertices_normal_texture = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getCubeFaceNormals(),  getTextureCords()))
v1 = shiftObjectVertices(vertices_normal_cube_colored, 0.6, 0.6)
v2 = shiftObjectVertices(vertices_normal_cube_colored, -0.6, 0.6)
v3 = shiftObjectVertices(vertices_normal_cube_colored, -0.6, -0.6)
v4 = shiftObjectVertices(vertices_normal_texture, 0.6, -0.6)

def main():
    pg.init()
    
    # # Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)  # Enable multisampling
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)  # Set the number of samples

    display = (800, 600)
    pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)

    camera = Camera(*display)
    light = Light()

    texture = Texture('textures/wood1.png')

    metall = Material(Type='metallic')
    dull = Material(Type='dull')
    bright = Material(Type='bright')
    bright_tex = Material(Type='bright', Texture=texture)

    shader = Shader('Shaders/defaultVertex.glsl', 'Shaders/defaultFragment.glsl')
    shader_tex = Shader('Shaders/texVert.glsl', 'Shaders/texFrag.glsl')

    cube1 = Shape(v1, metall, shader, ['3 0', '3 3', '3 6'], 9, rotatex = 0.2)
    cube2 = Shape(v2, dull, shader, ['3 0', '3 3', '3 6'], 9, rotatex = 0.2)
    cube3 = Shape(v3, bright, shader, ['3 0', '3 3', '3 6'], 9, rotatex = 0.2)
    cube4 = Shape(v4, bright_tex, shader_tex, ['3 0', '3 3', '2 6'], 8, rotatex = 0.2)

    renderer = Renderer([cube1, cube2, cube3, cube4], camera, light)

    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                renderer.destroy()
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    camera.zoom(1)
                elif event.button == 5:  # Scroll down
                    camera.zoom(-1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        renderer.render()
        pg.display.flip()

if __name__ == "__main__":
    main()

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
from FrameBuffer import FBO

vertices_normal_texture = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getCubeFaceNormals(), getTextureCords()))
plane_vertices = np.array([[-0.9, -0.9, 0, 0],
                           [-0.4, -0.9, 1, 0],
                           [-0.4, -0.4, 1, 1],
                           [-0.4, -0.4, 1, 1],
                           [-0.9, -0.4, 0, 1],
                           [-0.9, -0.9, 0, 0]])

v3 = shiftObjectVertices(vertices_normal_texture, -0.6)
v4 = shiftObjectVertices(vertices_normal_texture, 0.6)
pv = shiftObjectVertices(plane_vertices)


def main():
    pg.init()

    # # Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1) 
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)

    display = (500, 500)
    pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    pg.event.set_grab(True)
    pg.mouse.set_visible(False)

    camera = Camera(*display)
    staticCamera = Camera(*display, [0,-4,4], [0,4,-4])

    light = Light()

    texture = Texture('textures/wood2.png')
    texture_plane = Texture()

    bright_tex = Material(Type='bright', Texture=texture)
    dark = Material(Texture = texture_plane)

    shader_post_processing= Shader('Shaders/postVert.glsl', 'Shaders/PostFrag.glsl')
    # shader_light = Shader('Shaders/texVert.glsl', 'Shaders/texFrag.glsl')
    shader = Shader('Shaders/simpleVert.glsl', 'Shaders/simpleFrag.glsl')

    cube1 = Shape(v4, bright_tex, shader_post_processing, ['3 0', '3 3', '2 6'], 8)
    cube2 = Shape(v3, bright_tex, shader_post_processing, ['3 0', '3 3', '2 6'], 8, rotatex=0.1)
    plane = Shape(pv, dark, shader, ['2 0', '2 2'], 4)

    fbo = FBO(texture_plane)
    renderer = Renderer([cube1, cube2], camera, light, fbo, plane, staticCamera)

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
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        renderer.render()
        pg.display.flip()


if __name__ == "__main__":
    main()

    # shader_post_processing= Shader('Shaders/postVert.glsl', 'Shaders/PostFrag.glsl')
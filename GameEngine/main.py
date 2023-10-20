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
miniCamViewVertices = np.array([[-0.98, -0.98, 0, 0],
                                [-0.4, -0.98, 1, 0],
                                [-0.4, -0.4, 1, 1],
                                [-0.4, -0.4, 1, 1],
                                [-0.98, -0.4, 0, 1],
                                [-0.98, -0.98, 0, 0]])

floorTileVertices = np.array(getCombinedVertices(getFloorTileVertices(), getFloorTileIndices(), [0,0,1]*6, [0,0, 1,0 ,1,1 ,1,1 ,0,1 ,0,0], Index=True))

floorVertices = floorTileVertices

for i in range(50):
    for j in range(50):
        if i == j and j == 22:
            continue
        floorVertices = np.concatenate([floorVertices,shiftObjectVertices(floorTileVertices, x=i-22, z=j-22)], axis=0)
        # print(i,j)

v1 = shiftObjectVertices(vertices_normal_texture, -0.6)
mcvv = shiftObjectVertices(miniCamViewVertices)
fv = shiftObjectVertices(floorVertices, y=-1)

V = np.array(getObjectVertices("OBJs/man.obj"))
V = V.reshape(V.size//8, 8)
scaleObj = 0.01
vertObj = ScaleObjectVertices(V, scaleObj,scaleObj,scaleObj,5,6,7)
vertObj = shiftObjectVertices(vertObj, 0,-1.1,0,5,6,7)

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

    camera = Camera(*display)
    staticCamera = Camera(*display, [1,10,0], [-1,-10,0])

    light = Light([0,0,40])

    texture = Texture('textures/tile.jpg')
    textureMan = Texture('OBJs/man2/GLman_BaseColor.jpg')
    texture_plane = Texture(display=display)

    bright_tex = Material(Type='bright', Texture=texture)
    ManMaterial = Material(Texture=textureMan)
    dark = Material(Texture = texture_plane)

    shader_light = Shader('Shaders/texVert.glsl', 'Shaders/texFrag.glsl')
    shader = Shader('Shaders/simpleVert.glsl', 'Shaders/simpleFrag.glsl')

    obj = Shape(vertObj, ManMaterial, shader_light, ['in_tex_coord', 'in_normal', 'in_position'], ['2 0', '3 2', '3 5'], 8, rotatez=0.1, move=True)
    miniCam = Shape(mcvv, dark, shader, ['in_position', 'in_tex_coord'], ['2 0', '2 2'], 4)
    floorTile = Shape(fv, bright_tex, shader_light, ['in_position', 'in_normal', 'in_tex_coord'], ['3 0', '3 3', '2 6'], 8)

    fbo = FBO(texture_plane)
    renderer = Renderer([floorTile, obj], camera, light, fbo, miniCam, staticCamera)

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

        renderer.render()
        pg.display.flip()


if __name__ == "__main__":
    main()

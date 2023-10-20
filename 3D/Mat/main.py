import pygame as pg
import numpy as np
from OpenGL.GL import *
from Material import Material
from Light import Light
from Cube import Renderer
from Camera import Camera

def getCubeVertices():
    return [[-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            # Back face
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5]]

def getCubeIndices():
    return [ #Squares as faces
            0, 1, 2, 3,  #Front face
            4, 5, 6, 7,  #Back face
            0, 3, 7, 4,  #Left face
            1, 2, 6, 5,  #Right face
            0, 1, 5, 4,  #Bottom face
            2, 3, 7, 6   #Top face
        ]

def getWoodColor():
    return np.array([[130, 84, 59]*24])/255

def getCubeFacesColors():
    return np.array([[255, 0, 0] *4,
            [0, 255, 0] *4,
            [0, 0, 255] *4,
            [255, 255, 0] *4,
            [255, 0, 255] *4,
            [0, 255, 255] *4])/255

def getTextureCords():
    return np.array([[0,0, 0],[1,0, 0], [1,1, 0], [0,1, 0]]*6)

def getCubeFaceNormals():
    return [[0.0, 0.0, 1.0] *4,
            [0.0, 0.0, -1.0] *4,
            [-1.0, 0.0, 0.0] *4,
            [1.0, 0.0, 0.0] *4,
            [0.0, -1.0, 0.0] *4,
            [0.0, 1.0, 0.0] *4]

def getCombinedVertices(vertices, indices, *args):
    cubeVertices = np.array([vertices[i] for i in indices], dtype=np.float32)
    for ele in args:
        e = np.array(ele)
        cubeVertices = np.concatenate([cubeVertices, e.reshape(24, 3)], axis=1, dtype=np.float32)
    return cubeVertices

vertices_normal_cube_colored = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getCubeFacesColors(), getCubeFaceNormals()))
vertices_wood_colored = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getWoodColor(), getCubeFaceNormals()))
vertices_wood_texture = np.array(getCombinedVertices(getCubeVertices(), getCubeIndices(), getTextureCords(), getCubeFaceNormals()))
cube1 = Material(vertices_normal_cube_colored)
cube2 = Material(vertices_normal_cube_colored, 0.01, 0.8, 2)
cube3 = Material(vertices_normal_cube_colored, 0.2, 0.7, 0)
cube4 = Material(vertices_normal_cube_colored, 0.2, 0, 0)
cube5 = Material(vertices_normal_cube_colored, 0.2, 0, 2)
cube6 = Material(vertices_normal_cube_colored, 0, 0, 2)
cube7 = Material(vertices_normal_cube_colored, 1, 0, 0)
copper = Material(vertices_wood_colored)
wood = Material(vertices_wood_colored, 0.2, 0.8, 0, 0)
wood2 = Material(vertices_wood_texture, 0.2, 0.8, 0, 0)
R = cube1
def main():
    pg.init()
    
    # # Anti Aliasing
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)  # Enable multisampling
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)  # Set the number of samples


    display = (800, 600)
    pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    camera = Camera(*display)
    light = Light()
    cubeRenderer = Renderer(camera, light, R)
    # cubeRenderer = Renderer(camera, light, wood2, texture='Textures/wood2.png')

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                cubeRenderer.destroy()
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    camera.zoom(1)
                elif event.button == 5:  # Scroll down
                    camera.zoom(-1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cubeRenderer.draw()
        pg.display.flip()

if __name__ == "__main__":
    main()




# def shiftVertX(v, z):
#     return( np.array(list(map(lambda a: [*a[:2], a[2] + z, *a[3:]], v))))
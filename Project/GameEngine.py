import pygame as pg
from Camera import Camera
from FrameBuffer import FBO
from helpingFunctions import *
from Light import Light
from Material import Material
from OpenGL.GL import *
from Renderer import Renderer
from Shader import Shader
from Shape import Shape, Gun, Target
from Texture import Texture

class GameEngine:
    def __init__(self, display):
        self.display = display

        # ^ Cameras
        self.camera = Camera(*display, bgColor=[0.25,0.73,0.82])
        staticCamera = Camera(*display, [0, -0.32, -2.5], [0, 0, -20], bgColor=[0,0,0])

        # ^ Light
        light = Light([0, 40, 20])

        # ^ Textures
        texture = Texture('textures/Ground.jpg')
        textureGun = Texture('OBJs/Gun/ColtGunColourMap_2048.tif')
        textureTarget = Texture('OBJs/Target/Target.jpg')
        texture_plane = Texture(display=display)

        # ^ Materials
        bright_tex = Material(Type='bright', Texture=texture)
        GunMaterial = Material(Texture=textureGun)
        TargetMaterial = Material(Texture=textureTarget)
        dark = Material(Texture=texture_plane)
        emptyMat = Material()

        # ^ Shaders
        shader_light = Shader('Shaders/texVert.glsl', 'Shaders/texFrag.glsl')
        shader = Shader('Shaders/simpleVert.glsl', 'Shaders/simpleFrag.glsl')
        defaultShader = Shader('Shaders/defaultVertex.glsl', 'Shaders/defaultFragment.glsl')

        # ^ Shapes
        # ~ Vertices (Data) Orientation, formats
        VO1, F1 = ['in_position', 'in_normal', 'in_tex_coord'], ['3 0', '3 3', '2 6']
        VO2, F2 = ['in_tex_coord', 'in_normal', 'in_position'], ['2 0', '3 2', '3 5']
        VO3, F3 = ['in_position', 'in_tex_coord'], ['2 0', '2 2']
        # * Gun
        translateGun = [0, -0.22, 3.6]
        GunVertices = getOBJVerticesOriented("OBJs/Gun/Gun.obj", translateGun, 0.005, [0,180,0])
        self.gun = Gun(GunVertices, GunMaterial, shader_light, VO2, F2, 8, translated=translateGun, xpos=5,bulletParams = [emptyMat, defaultShader])
        # * Target
        TargetVertices = getOBJVerticesOriented("OBJs/Target/Target.obj", [0, -0.9, -4], rotation=[66,0,0])
        self.target = Target(TargetVertices, TargetMaterial, shader_light, VO2, F2, 8)
        # * MiniCamView
        miniCamViewVertices = createMiniCam()
        miniCamScreen = Shape(miniCamViewVertices, dark, shader, VO3, F3, 4)
        fbo = FBO(texture_plane)
        # * Floor
        floorVertices = createFloor(10)
        floorTile = Shape(floorVertices, bright_tex, shader_light, VO1, F1, 8)

        self.renderer = Renderer([self.gun, floorTile, self.target], self.camera, light, fbo, miniCamScreen, staticCamera)
        glEnable(GL_DEPTH_TEST)

    def start(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.renderer.destroy()
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.camera.zoom(1)
                    elif event.button == 5:  # Scroll down
                        self.camera.zoom(-1)
                    elif event.button == 1: #^ click
                        self.gun.fire()

            for b in self.gun.bullets:
                b.move()
            self.renderer.render()

            pg.display.flip()

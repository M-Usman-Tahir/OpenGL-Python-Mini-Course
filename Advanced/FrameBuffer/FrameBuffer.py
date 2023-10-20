from OpenGL.GL import *

class FBO:
    def __init__(self, tex) -> None:
        self.depth_buff = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_buff)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, tex.width, tex.height)

        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex.texture_id, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_buff)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def destroy(self):
        glDeleteRenderbuffers(1, (self.depth_buff,)) 
        glDeleteFramebuffers(1, (self.fbo,))
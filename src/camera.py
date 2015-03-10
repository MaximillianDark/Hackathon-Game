"""Camera class."""

from ctypes import byref

import lib.sdl2 as sdl2

from src.sprite import Sprite
from src.gfx import Rect

class Camera(Sprite):
    """Camera class implements the transition between game space and screen."""
    def __init__(self, startpos, sheet, renderer):
        """
        
        startpos is the center of the camera's viewrect in gamespace."""
        self.sheet = sheet
        self.renderer = renderer
        self.src = Rect(0, 0, 640, 480)
        self.src.center = startpos
        self.dest = Rect(0, 0, 640, 480)
        super(Camera, self).__init__(self.src, self.dest)
        
    def update(self, controller):
        if controller.keys["w"] == True:
            self.src.y -= 8
        elif controller.keys["s"]:
            self.src.y += 8
        if controller.keys["a"]:
            self.src.x -= 8
        elif controller.keys["d"]:
            self.src.x += 8
            
    def render(self, src, dest):
        transrect = Rect(dest.x-self.src.x, dest.y-self.src.y, dest.w, dest.h)
        self.renderer.render(self.sheet, src, transrect)
            
    def render_all(self, world):
        for sprite in world.spritelist:
            if sdl2.SDL_HasIntersection(byref(self.src), byref(sprite.dest)):
                sprite.render(self)
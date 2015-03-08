"""Camera class."""

from ctypes import byref

import lib.sdl2 as sdl2

from src.sprite import Sprite
from src.gfx import Rect

class Camera(Sprite):
    """Camera class."""
    def __init__(self, startpos, sheet):
        self.sheet = sheet
        self.src = Rect(startpos[0], startpos[1], 640, 480)
        self.dest = Rect(0, 0, 640, 480)
        super(Camera, self).__init__(self.src, self.dest)
        
    def update(self, controller):
        print((self.src.x, self.src.y))
        if controller.keys["w"] == True:
            self.src.y -= 8
        elif controller.keys["s"]:
            self.src.y += 8
        if controller.keys["a"]:
            self.src.x -= 8
        elif controller.keys["d"]:
            self.src.x += 8
            
    def render(self, renderer, world):
        for sprite in world.spritelist:
            if sdl2.SDL_HasIntersection(byref(self.src), byref(sprite.dest)):
                transrect = Rect(sprite.dest.x-self.src.x, sprite.dest.y-sprite.dest.y, sprite.dest.w, sprite.dest.h)
                renderer.render(self.sheet.tex, sprite.src, transrect)
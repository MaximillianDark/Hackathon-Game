"""Controller class."""

import lib.sdl2 as sdl2

class Controller:
    def __init__(self, keys):
        self.keys = dict(keys, [False]*len(keys))
    
    def update(e):
        if e.keysym in self.keys.keys:
            if e.type == sdl2.SDL_KEYDOWN: 
                self.keys[e.keysym] = True
            elif e.type == sdl2.SDL_KEYUP:
                self.keys[e.keysym] = False
        
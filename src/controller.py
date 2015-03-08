"""Controller class."""

import lib.sdl2 as sdl2

class Controller:
    def __init__(self, keys):
        self.keys = {"w":False, "s":False, "a":False, "d":False}
    
    def update(self, e):
        #print((e.type, e.key.keysym.sym))
        if e.type == sdl2.SDL_KEYDOWN: 
            if e.key.keysym.sym == sdl2.SDLK_w:
                self.keys["w"] = True
            elif e.key.keysym.sym == sdl2.SDLK_s:
                self.keys["s"] = True
            elif e.key.keysym.sym == sdl2.SDLK_a:
                self.keys["a"] = True
            elif e.key.keysym.sym == sdl2.SDLK_d:
                self.keys["d"] = True
        elif e.type == sdl2.SDL_KEYUP:
            if e.key.keysym.sym == sdl2.SDLK_w:
                self.keys["w"] = False
            elif e.key.keysym.sym == sdl2.SDLK_s:
                self.keys["s"] = False
            elif e.key.keysym.sym == sdl2.SDLK_a:
                self.keys["a"] = False
            elif e.key.keysym.sym == sdl2.SDLK_d:
                self.keys["d"] = False
        #print(self.keys)
    
    def _find_key(self, key):
        c = 0
        for p in self.keys:
            if key == p[0]:
                print((key, self.keys[c]))
                return c
            c += 1
            
    def _get_keysym(self, name):
        return getattr(sdl2, "SDLK_"+name, None)
        
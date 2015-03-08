"""Wrapper around pysdl2, since that pythonic wrapper is confusing."""

import os
from ctypes import cast, POINTER, c_uint32, c_uint8, byref

os.environ["PYSDL2_DLL_PATH"] = "lib\\"

import lib.sdl2 as sdl2

def init(flags=0):
    sdl2.SDL_Init(flags)

def quit():
    sdl2.SDL_Quit()
    
def get_pix(surf, x, y):
    Bpp = surf.format.contents.BytesPerPixel
    pixs = cast(surf.pixels, POINTER(c_uint8))
    addr = x*Bpp+y*surf.pitch
    if sdl2.SDL_BYTEORDER == sdl2.SDL_LIL_ENDIAN:
        pix = sum([pixs[addr+i]<<(8<<i) for i in range(Bpp)])
    else: # endianess correc tfinding of an unknown number of bytes
        pix = sum([pixs[addr+i]<<(8<<(Bpp-(i))) for i in range(Bpp)])
    r = c_uint8(0)
    g = c_uint8(0)
    b = c_uint8(0)
    print(pix)
    sdl2.SDL_GetRGB(c_uint32(pix), surf.format, r, g, b)
    return r.value, g.value, b.value

class Window:   
    """Wrap the relevant functions in pysdl2 to implement windows."""
    def __init__(self, title, size, pos=(sdl2.SDL_WINDOWPOS_UNDEFINED,)*2, f=0):
        w, h = size
        x, y = pos
        self._win = sdl2.SDL_CreateWindow(bytes(title, "UTF-8"), x, y, w, h, f)
    def __del__(self):
        sdl2.SDL_DestroyWindow(self._win)

class Texture:
    def __init__(self, renderer, filename):
        surf = sdl2.SDL_LoadBMP(bytes(filename ,"UTF-8"))
        sdl2.SDL_SetColorKey(surf, 1, sdl2.SDL_MapRGB(surf.contents.format, 255, 0, 0))
        self._tex = sdl2.SDL_CreateTextureFromSurface(renderer._ren, surf)
        sdl2.SDL_FreeSurface(surf)
    def __del__(self):
        sdl2.SDL_DestroyTexture(self._tex)
    
class Renderer:
    def __init__(self, window, driver=-1, flags=0): 
        self._ren = sdl2.SDL_CreateRenderer(window._win, driver, flags)
    def __del__(self):
        sdl2.SDL_DestroyRenderer(self._ren)
        
    def render(self, tex, src, dest):
        sdl2.SDL_RenderCopy(self._ren, tex._tex, src, dest)
    def present(self):
        sdl2.SDL_RenderPresent(self._ren)
    def clear(self):
        sdl2.SDL_RenderClear(self._ren)

class Rect(sdl2.SDL_Rect):
    def __init__(self, *args):
        super(Rect, self).__init__(*args)
    def __getattribute__(self, name):
        return getattr(super(Rect, self), name)
    def __setattribute__(self, name, val):
        return setattr(super(Rect, self), name, val)
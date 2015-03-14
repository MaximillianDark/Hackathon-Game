"""Wrapper around pysdl2, since that pythonic wrapper is confusing."""

import os
from ctypes import cast, POINTER, c_uint32, c_uint8, byref

import math

os.environ["PYSDL2_DLL_PATH"] = "lib\\"

import lib.sdl2 as sdl2

def init(flags=0):
    sdl2.SDL_Init(flags)

def quit():
    sdl2.SDL_Quit()

class Window:   
    """Wrap the relevant functions in pysdl2 to implement windows."""
    def __init__(self, title, size, pos=(sdl2.SDL_WINDOWPOS_UNDEFINED,)*2, f=0):
        w, h = size # split assignments
        x, y = pos
        self._win = sdl2.SDL_CreateWindow(bytes(title, "UTF-8"), x, y, w, h, f)
        # internal pointer reference
    def __del__(self):
        sdl2.SDL_DestroyWindow(self._win)

class Texture:
    """Pythonic wrapper for SDL's textures"""
    def __init__(self, renderer, filename):
        surf = sdl2.SDL_LoadBMP(bytes(filename ,"UTF-8"))
        sdl2.SDL_SetColorKey(surf, 1, sdl2.SDL_MapRGB(surf.contents.format, 255, 0, 0)) ## TODO: fix magic color value/colorkeying in general
        self._tex = sdl2.SDL_CreateTextureFromSurface(renderer._ren, surf)
        sdl2.SDL_FreeSurface(surf)
    def __del__(self):
        sdl2.SDL_DestroyTexture(self._tex)
    
class Renderer:
    """Pythonic wrapper of relevant SDL_Renderer"""
    def __init__(self, window, driver=-1, flags=0): 
        self._ren = sdl2.SDL_CreateRenderer(window._win, driver, flags)
    def __del__(self):
        sdl2.SDL_DestroyRenderer(self._ren)
        
    def render(self, tex, src, dest):
        """copies tex subsection src to screen buffer at dest"""
        sdl2.SDL_RenderCopy(self._ren, tex._tex, src, dest)
    def present(self):
        """shows the graphics that have been written to screen."""
        sdl2.SDL_RenderPresent(self._ren)
    def clear(self):
        """wipes current buffer to single value"""
        sdl2.SDL_RenderClear(self._ren)

class Rect(sdl2.SDL_Rect):
    """Wraps SDL_Rect"""
    def __init__(self, *args):
        super(Rect, self).__init__(*args)
        
    def __getattribute__(self, name):
        """Implements all the attributes by calculating most of them."""
        get = lambda n: getattr(super(Rect, self), n) # because super only redirects methods
        if name in ("x", "y", "w", "h"): # Base attributes, need to directly access the struct
            return get(name)
        elif name == "center":
            return (get("x") + (get("w") // 2), (get("y") + get("h") // 2))
        elif name == "left": # same as x, more descriptive
            return get("x")
        elif name == "right": # right side of rect, x+w
            return get("x")+get("w")
        elif name == "top": # same as y
            return get("y")
        elif name == "bottom": # top plus height (reversed y)
            return get("y")+get("h")
        else:
            raise AttributeError(name+" is not a valid Rect attribute")
            
    def __setattr__(self, name, val):
        set = lambda n, v: super(Rect, self).__setattr__(n, v) # because super only redirects methods
        get = lambda n: getattr(super(Rect, self), n) # see above line
        if name in ("x", "y", "w", "h"): # Base attributes, need to directly access the struct
            set(name, val)
        elif name == "center": # need to subtract half height and width from val[0] and val[1] before setting x and y
            set("x", val[0] - (get("w") // 2))
            set("y", val[1] - (get("h") // 2))
        elif name == "left": # same as x, more descriptive
            set("x", val)
        elif name == "right": # right side of rect, set x to val minus width
            set("x", val - get("w"))
        elif name == "top": # same as y
            set("y", val)
        elif name == "bottom": # top equals val minus height (reversed y)
            set("y", val - get("h"))
        else:
            raise AttributeError(name+" is not a valid Rect attribute")
    def intersects(other):
        if not isinstance(other, Rect):
            raise TypeError("trying to intersect rect with non rect "+str(other))
        if sdl2.SDL_HasIntersection(self, other) == sdl2.SDL_TRUE:
            return True
        else:
            return False
            
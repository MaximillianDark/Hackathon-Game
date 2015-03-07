"""SDL2 Wrapper for this project."""

from ctypes import *

sdl2 = CDLL("lib/SDL2.dll")

## Constants ##
WIN_CENTERED = 0x2FFF0000

## Structures ##
class SDL_Window(Structure):
    _fields_ = []

## ll_methods ##

# SDL.h
sdl2.SDL_Init.argtypes = [c_uint]
sdl2.SDL_Init.restype = c_int

sdl2.SDL_Quit.argtypes = []
#sdl2.SDL_Quit.restype is void

# SDL_video.h
sdl2.SDL_CreateWindow.argtypes = [c_char_p,\
                                  c_int,\
                                  c_int,\
                                  c_int,\
                                  c_int,\
                                  c_uint]
sdl2.SDL_CreateWindow.restype = POINTER(SDL_Window)

sdl2.SDL_DestroyWindow.argtypes = [POINTER(SDL_Window)]
#sdl2.SDL_DestroyWindow.restype is void

sdl2.SDL_GetWindowSize.argtypes = [POINTER(SDL_Window),\
                                   POINTER(c_int),\
                                   POINTER(c_int)]
#sdl2.SDL_GetWindowSize.restype is void

sdl2.SDL_GetWindowPosition.argtypes = [POINTER(SDL_Window),\
                                    POINTER(c_int),\
                                    POINTER(c_int)]
#sdl2.SDL_GetWindowPositionrestype is void

sdl2.SDL_SetWindowSize.argtypes = [POINTER(SDL_Window),\
                                   c_int,\
                                   c_int]
#sdl2.SDL_SetWindowSize.restype is void

## Wrapper functions ##

def init(flags):
    """Initialize SDL Library"""
    return sdl2.SDL_Init(c_uint(flags))
    
def quit(): 
    """Uninitialize SDL Library"""
    sdl2.SDL_Quit()
    
class Window:
    """Wrapper for the window related sdl functions"""
    def __init__(self, title, pos, size, flags):
        self._win = sdl2.SDL_CreateWindow(bytes(title, "UTF-8"),\
                                          pos[0], pos[1],\
                                          size[0], size[1],\
                                          c_uint(flags))
    def __del__(self):
        sdl2.SDL_DestroyWindow(self._win)
        
    def __getattr__(self, name):
        if name == "size":
            w = pointer(c_int)
            h = pointer(c_int)
            sdl2.SDL_GetWindowSize(self._win, w, h)
            return (w.contents.value, h.contents.value)
        elif name == "pos":
            x = pointer(c_int)
            y = pointer(c_int)
            sdl2.SDL_GetWindowPos(self._win, x, y)
            return (x.contents.value, y.contents.value)
                
    def __setattr__(self, name, val):
        if name == "size":
            sdl2.SDL_SetWindowSize(self._win, val[0], val[1])
        if name == "pos":
            sdl2.SDL_SetWindowPosition(self._win, val[0], val[1])
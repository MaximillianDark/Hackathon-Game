"""SDL2 Wrapper for this project."""

from ctypes import *

sdl2 = CDLL("lib/SDL2.dll")

## Constants ##
WIN_CENTERED = 0x2FFF0000

## Structures ##
class SDL_Window(Structure):
    _fields_ = []
SDL_Window_p = POINTER(SDL_Window)
    
class SDL_Renderer(Structure)
    _fields_ = []
SDL_Renderer_p = POINTER(SDL_Renderer)
    
class SDL_Texture(Structure)
    _fields_ = []
SDL_Texture_p = POINTER(SDL_Texture)

class SDL_Surface(Structure)
    _fields_ = []
SDL_Surface_p = POINTER(SDL_Surface)
    
class SDL_Point(Structure):
    _fields_ = [("x", c_int32),\
                ("y", c_int32)]
SDL_Point_p = POINTER(SDL_Point)
                
class SDL_Rect(Structure):
    _fields_ = [("x", c_int32),\
                ("y", c_int32),\
                ("w", c_int32),\
                ("h", c_int32)]
SDL_Rect_p = POINTER(SDL_Rect)
                
SDL_Bool = c_int8 # Enum that is either 1 or 0

## ll_methods ##

# SDL.h
sdl2.SDL_Init.argtypes = [c_uint32]
sdl2.SDL_Init.restype = c_int32

sdl2.SDL_Quit.argtypes = []
#sdl2.SDL_Quit.restype is void

# SDL_video.h
sdl2.SDL_CreateWindow.argtypes = [c_char_p,\
                                  c_int32,\
                                  c_int32,\
                                  c_int32,\
                                  c_int32,\
                                  c_uint32]
sdl2.SDL_CreateWindow.restype = SDL_Window_p

sdl2.SDL_DestroyWindow.argtypes = [SDL_Window_p]
#sdl2.SDL_DestroyWindow.restype is void

sdl2.SDL_GetWindowSize.argtypes = [SDL_Window_p,\
                                   POINTER(c_int32),\
                                   POINTER(c_int32)]
#sdl2.SDL_GetWindowSize.restype is void

sdl2.SDL_GetWindowPosition.argtypes = [SDL_Window_p,\
                                    POINTER(c_int32),\
                                    POINTER(c_int32)]
#sdl2.SDL_GetWindowPositionrestype is void

sdl2.SDL_SetWindowSize.argtypes = [SDL_Window_p,\
                                   c_int32,\
                                   c_int32]
#sdl2.SDL_SetWindowSize.restype is void

# SDL_Rect.h
sdl2.SDL_HasIntersection.argtypes = [SDL_Rect_p,\
                                     SDL_Rect_p]
sdl2.SDL_HasIntersection.restype = SDL_Bool

# SDL_Renderer.h
sdl2.SDL_CreateRenderer.argtypes = [SDL_Window_p,\
                                    c_int,\
                                    c_uint32]
sdl2.SDL_CreateRenderer.restype = SDL_Renderer_p

sdl2.SDL_DestroyRenderer.argtypes = [SDL_Renderer_p]
#sdl2.SDL_DestroyRenderer.restype is void

sdl2.SDL_CreateTextureFromSurface.argtypes = [SDL_Renderer_p,\
                                              SDL_Surface_p]
sdl2.SDL_CreateTextureFromSurface.restype = SDL_Texture_p

SDL2.SDL_DestroyTexture.argtypes = [SDL_Texture_p]
#sdl2.SDL_DestroyTexture.restype is void

sdl2.SDL_RenderCopy.argtypes = [SDL_Renderer_p,\
                                SDL_Texture_p,\
                                SDL_Rect_p,\
                                SDL_Rect_p,\
sdl2.SDL_RenderCopy.restype = c_int

sdl2.SDL_RenderClear.argtypes = [SDL_Renderer_p]
sdl2.SDL_RenderClear.restype = c_int

sdl2.SDL_LoadBMP.argtypes = [c_char_p]
sdl2.SDL_LoadBMP.restype = SDL_Surface_p

sdl2.SDL_DestroySurface.argtypes = [SDL_Surface_p]
#sdl2.SDL_DestroySurface.restype is void

## Wrapper functions ##

def init(flags):
    """Initialize SDL Library"""
    return sdl2.SDL_Init(c_uint32(flags))
    
def quit(): 
    """Uninitialize SDL Library"""
    sdl2.SDL_Quit()
    
class Window:
    """Wrapper for the window related sdl functions"""
    def __init__(self, title, pos, size, flags):
        self._win = sdl2.SDL_CreateWindow(bytes(title, "UTF-8"),\
                                          pos[0], pos[1],\
                                          size[0], size[1],\
                                          c_uint32(flags))
    def __del__(self):
        sdl2.SDL_DestroyWindow(self._win)
        
    def __getattr__(self, name):
        if name == "size":
            w = pointer(c_int32)
            h = pointer(c_int32)
            sdl2.SDL_GetWindowSize(self._win, w, h)
            return (w.contents.value, h.contents.value)
        elif name == "pos":
            x = pointer(c_int32)
            y = pointer(c_int32)
            sdl2.SDL_GetWindowPos(self._win, x, y)
            return (x.contents.value, y.contents.value)
                
    def __setattr__(self, name, val):
        if name == "size":
            sdl2.SDL_SetWindowSize(self._win, val[0], val[1])
        if name == "pos":
            sdl2.SDL_SetWindowPosition(self._win, val[0], val[1])

class Renderer:
    """Wrapper for the sdl renderer functions"""
    def __init__(self, window, driver, flags):
        self._renderer = sdl2.SDL_CreateRenderer(window, driver, flags)
    def __del__(self):
        sdl2.SDL_DestroyRenderer(self._renderer)
    
    def render_copy(self, tex, src, dst):
        """SDL_RenderCopy copies pixels in tex to screen from src to dst"""
        sdl2.SDL_RenderCopy(self._renderer, tex, src, dst)
    
    def render_clear(self): 
        sdl2.SDL_RenderClear(self._renderer)

class Texture:
    """Wrapper for SDL_Texture"""
    def __init__(self, filename, renderer):
        surf = sdl2.SDL_LoadBMP(bytes(filename, "UTF-8"))
        self._tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
        sdl2.SDL_DestroySurface(surf)
    def __del__(self):
        sdl2.SDL_DestroyTexture(self._tex)
    
    def from_param(obj):
        if isinstance(obj, Texture):
            return obj._tex
        else:
           raise TypeError("Passed non-Texture to Texture.from_param")
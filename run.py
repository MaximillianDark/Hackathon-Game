#! /usr/bin/python3
"""Startup file for the hackathon game.

Date: 2015-03-07
Authors: PythonJedi, jkwiedman"""

import time

print("I'm alive!")

## The following is just testing of ctypes module. It will be moved to lib.

import ctypes

class SDL_Window(ctypes.Structure):
    _fields_ = []

sdl2 = ctypes.CDLL("lib/SDL2.dll")

sdl2.SDL_CreateWindow.restype = ctypes.POINTER(SDL_Window)
sdl2.SDL_CreateWindow.argtypes = [ctypes.c_char_p,\
                                  ctypes.c_int,\
                                  ctypes.c_int,\
                                  ctypes.c_int,\
                                  ctypes.c_int,\
                                  ctypes.c_uint]
                                  
sdl2.SDL_Init(0)

sdl2.SDL_CreateWindow(b"Testing Window!", 100, 100, 640, 480, 0)

time.sleep(5)

sdl2.SDL_Quit()
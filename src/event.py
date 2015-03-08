"""Wrapper for events stuff."""

import lib.sdl2 as sdl2
from ctypes import byref

def get_events():
    events = []
    e = sdl2.SDL_Event()
    while sdl2.SDL_PollEvent(byref(e)):
        events.append(e)
    return events
"""Wrapper for events stuff."""

import lib.sdl2 as sdl2
from ctypes import byref

class Event(sdl2.SDL_Event):
    def __init__(self, *args):
        super(Event, self).__init__(*args)
    def __getattribute__(self, name):
        return getattr(super(Event, self), name)
    def __setattribute__(self, name, val):
        return setattr(super(Event, self), name, val)

def poll(e):
    return sdl2.SDL_PollEvent(byref(e))
    
def push(e):
    return sdl2.SDL_PushEvent(byref(e))
#! /usr/bin/python3
"""Startup file for the hackathon game.

Date: 2015-03-07
Authors: PythonJedi, jkwiedman"""

# stdlib imports
import time, os

# project imports
import src.gfx as gfx
import src.event as event
import lib.sdl2 as sdl2 # need event constants

gfx.init()

win = gfx.Window("testing", (640, 480))
ren = gfx.Renderer(win)
tex = gfx.Texture(ren, "res\\game-tiles.bmp")
rect = gfx.Rect(0, 0, 640, 480)

ren.render(tex, rect, rect)
ren.present()
running = True
while running:
    for e in event.get_events():
        if e.type == sdl2.SDL_QUIT:
            running = False
            break

del(rect)
del(tex)
del(ren)
del(win)

gfx.quit()
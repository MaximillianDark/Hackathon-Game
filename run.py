#! /usr/bin/python3
"""Startup file for the hackathon game.

Date: 2015-03-07
Authors: PythonJedi, jkwiedman"""

# stdlib imports
import time, os

# project imports
import src.gfx as gfx
import src.event as event
import res.res as res
from src.entity import Seed
import lib.sdl2 as sdl2 # need event constants

def main():
    gfx.init()

    win = gfx.Window("testing", (640, 480))
    ren = gfx.Renderer(win)
    sheet = res.SpriteSheet(gfx.Texture(ren, "res\\game-tiles.bmp"))
    
    lev, start, seeds = res.load_level("res\\Test-Level.bmp", sheet)
    print(lev)
    print()
    print(start)
    print()
    print(seeds)
    
    obj = Seed(sheet, (100, 100))

    running = True
    e = event.Event()
    while running:
        while event.poll(e):
            if e.type == sdl2.SDL_QUIT:
                running = False
                break
        obj.update()
        ren.clear()
        obj.render(ren)
        ren.present()
        time.sleep(0.1)
        
    del(obj)
    del(sheet)
    del(ren)
    del(win)

    gfx.quit()
    
if __name__ == "__main__":
    main()
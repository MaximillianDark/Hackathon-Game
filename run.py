#! /usr/bin/python3
"""Startup file for the hackathon game.

Date: 2015-03-07
Authors: PythonJedi, jkwiedman"""

# stdlib imports
import time

# project imports
import lib.sdl2 as sdl2


print("I'm alive!")

sdl2.init(0)
win = sdl2.Window("Testing sdl2 wrapper", (sdl2.WIN_CENTERED,)*2, (640, 480), 0)
time.sleep(5)
del(win)
sdl2.quit()
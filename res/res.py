"""Spritesheet class for accessing subsections of the spritesheet."""

from src.gfx import Rect, Texture
from src.util import *
from src.sprite import Group
from src.tile import Tile
import src.entity as entity
import lib.sdl2 as sdl2 # importing gfx module first ensures sdl2 is loaded already
        
def read_level(file):   
    return [l for l in file]
    
def load_level(filename, sheet):
    lev = Group()
    seeds = Group()
    checkpoints = Group()
    start = None
    end = None
    f = open(filename, newline="")
    d = read_level(f)
    f.close()
    
    for y in range(len(d)):
        for x in range(len(d[y])):
            p = d[y][x]
            if _tile_type(p) == "Platform":
                src = _tile_find((x, y), d, sheet)
                lev.add(Tile(sheet, src, tile2rect((x, y))))
            elif _tile_type(p) == "Seed":
                pos = tile2rect((x, y))
                seeds.add(entity.Seed(sheet, (pos.x, pos.y)))
            elif _tile_type(p) == "Start":
                start = tile2rect((x, y))  
            elif _tile_type(p) == "End":
                pos = tile2rect((x, y))
                end = entity.End(sheet, (pos.x, pos.y))
            elif _tile_type(p) == "Checkpoint":
                pos = tile2rect((x, y))
                checkpoints.add(entity.Checkpoint(sheet, (pos.x, pos.y)))
    return lev, start, end, seeds, checkpoints
    
def _tile_type(data):
    if data == "t":
        return "Platform"
    elif data == "s":
        return "Start"
    elif data == "e":
        return "End"
    elif data == "p":
        return "Seed"
    elif data == "c":
        return "Checkpoint"
    else:
        return ""
    
def _tile_find(pos, level_data, sheet):
    # need to see the surrounding tiles
    src = "" # part of what I will pass to tile constructor
    x, y = pos
    # check horizontal tiles
    if x == len(level_data[y])-1: # right side, left tile
        src = "l"
    elif x == 0: # left side, right tile
        src = "r"
    elif _tile_type(level_data[y][x-1])=="Platform": # tile on left
        if _tile_type(level_data[y][x+1])== "Platform": # tile on right
            src = "c" # horizontal center tile
        else: # only tile on left
            src = "r" # right tile
    elif _tile_type(level_data[y][x+1]) == "Platform": # only tile on right
        src = "l" # left tile
    else: # no tile either side
        src = "c" # until I actually have a hoizontal center tile
    
    # check vertical tiles
    if y == len(level_data)-1: # bottom of map, upper tile
        src = src+"t"
    elif y == 0: # top of map, lower tile
        src = src+"l"
    elif _tile_type(level_data[y-1][x]) == "Platform": # tile above
        if _tile_type(level_data[y+1][x]) == "Platform": # tile below
            # vertical center tile
            src = src+"c"
        else: # only tile above
            #lower tile
            src = src+"l"
    elif _tile_type(level_data[y+1][x]) == "Platform" : # only tile below
        # upper tile
        src = src + "t"

    return getattr(sheet.platform, src)
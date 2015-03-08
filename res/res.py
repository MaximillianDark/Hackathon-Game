"""Spritesheet class for accessing subsections of the spritesheet."""

from src.gfx import Rect, Texture
from src.sprite import Group
from src.tile import Tile
import lib.sdl2 as sdl2 # importing gfx module first ensures sdl2 is loaded already

SCALE = 32

def _tile2rect(pos, size=(1, 1)):
    """Return a rect given tile coordiantes."""
    return Rect(pos[0]*SCALE, pos[1]*SCALE, size[0]*SCALE, size[1]*SCALE)

class Platform:
    class OneThick:
        def __getattr__(self, name):
            if name == "l": # Left
                return _tile2rect((0, 0))
            elif name == "c": # Center 
                return _tile2rect((1, 0))
            elif name == "r": # Right
                return _tile2rect((2, 0))
            else:
                raise AttributeError("Invalid attribute for one thick tile")
        
    class TwoThick:
        def __getattr__(self, name):
            if len(name) != 2:
                raise AttributeError("Invalid attribute for two thick tile")
            else:
                if name[0] == "u": # Upper
                    y = 1
                elif name[0] == "l": # Lower
                    y = 2
                else:
                    raise AttributeError("Invalid attribute for two thick tile")
                if name[1] == "l": # Left
                    x = 0
                elif name[1] == "c": # Center 
                    x = 1
                elif name[1] == "r": # Right
                    x = 2
                else:
                    raise AttributeError("Invalid attribute for two thick tile")
            return _tile2rect((x, y))
        
    class ThreeThick:
        def __getattr__(self, name):
            if len(name) != 2:
                raise AttributeError("Invalid attribute for three thick tile")
            else:
                if name[0] == "u": # Upper
                    y = 0
                elif name[0] == "c":
                    y = 1
                elif name[0] == "l": # Lower
                    y = 2
                else:
                    raise AttributeError("Invalid attribute for three thick tile")
                if name[1] == "l": # Left
                    x = 3
                elif name[1] == "c": # Center 
                    x = 4
                elif name[1] == "r": # Right
                    x = 5
                else:
                    raise AttributeError("Invalid attribute for three thick tile")
            return _tile2rect((x, y))

            
    def __init__(self):
        self.one_thick = Platform.OneThick()
        self.two_thick = Platform.TwoThick()
        self.three_thick = Platform.ThreeThick()
    
class Player:
    class Walk:
        frames = (0, 2, 0, 3)
        class Right:
            def __getitem__(self, index):
                if index in range(4):
                    return _tile2rect((6, Walk.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        class Left:
            def __getitem__(self, index):
                if index in range(4):
                    return _tile2rect((7, Walk.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        def __init__(self):
            self.right = Player.Walk.Right()
            self.left = Player.Walk.Left()
            
    class Stand:
        frames = (0, 1)
        class Right:
            def __getitem__(self, index):
                if index in range(2):
                    return _tile2rect((6, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
                
        class Left:
            def __getitem__(self, index):
                if index in range(2):
                    return _tile2rect((7, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
                    
        def __init__(self):
            self.right = Player.Stand.Right()
            self.left = Player.Stand.Left()
        
    class Jump:
        frames = (0, 4, 5, 6, 0)
        class Right:
            def __getitem__(self, index):
                if index in range(5):
                    return _tile2rect((6, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        class Left:
            def __getitem__(self, index):
                if index in range(5):
                    return _tile2rect((7, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        def __init__(self): 
            self.right = Player.Jump.Right()
            self.left = Player.Jump.Left()
    
    def __init__(self):
        self.walk = Player.Walk()
        self.stand = Player.Stand()
        self.jump = Player.Jump()
    
class End:
    def __getitem__(self, index):
        if index in (0, 1, 2):
            return _tile2rect((3, 3+index))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class Checkpoint:
    def __getitem__(self, index):
        if index in (0, 1, 2):
            return _tile2rect((index, 4), (1, 2))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class Seed:
    def __getitem__(self, index):
        if index in (0, 1, 2):
            return _tile2rect((index, 3))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class SpriteSheet:
    def __init__(self, tex):
        self.tex = tex
        self.player = Player()
        self.platform = Platform()
        self.end = End()
        self.seed = Seed()
        self.checkpoint = Checkpoint()
        
def load_level(filename):
    lev = Group()
    surf = sdl2.SDL_LoadBMP(bytes(filename, "UTF-8"))
    
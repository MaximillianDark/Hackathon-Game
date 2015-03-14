"""Sprite module for the project."""
    
from src.util import *

class Sprite:
    """Base sprite class for onscreen objects."""
    def __init__(self, src, dest, groups=None):
        self.src = src
        self.dest = dest
        self.groups = []
        if groups:
            for g in groups:
                g.add(self)
    def _add(self, group):
        if group not in self.groups:
            self.groups.append(group)
    def _remove(self, group):
        if group in self.groups:
            self.groups.remove(group)
    
    def update(self, *args):
        pass
        
    def render(self, renderer):
        pass
    
    def kill(self):
        for g in self.groups:
            g.remove(self)
            
    def intersects(self, other):
        return self.dest.intersects(other.dest)
    
        
class Group:
    """Grouping class for nicely handling sprites"""
    def __init__(self, sprites=None):
        self.spritelist = []
        if sprites:
            for s in sprites:
                self.add(s)
    
    def add(self, sprite):
        if sprite not in self.spritelist:
            self.spritelist.append(sprite)
        if self not in sprite.groups:
            sprite._add(self)
    
    def append(self, other):
        """Add other group's sprites to this group."""
        for s in other.spritelist:
            self.add(s)
    
    def remove(self, sprite):
        if sprite in self.spritelist:
            self.spritelist.remove(sprite)
            sprite._remove(self)
            
    def update(self, *args):
        for sprite in self.spritelist:
            sprite.update(*args)
    
    def render(self, renderer):
        for sprite in self.spritelist:
            sprite.render(renderer)
    def collide_with(self, other):
        return [sprite for sprite in self.spritelist if sprite.intersects(other)]
            
    def __str__(self):
        return str(self.spritelist)
        
class Platform:
    def __getattr__(self, name):
        if len(name) == 1:
            if name == "l": # Left
                return tile2rect((0, 0))
            elif name == "c": # Center 
                return tile2rect((1, 0))
            elif name == "r": # Right
                return tile2rect((2, 0))
            else:
                raise AttributeError("Invalid attribute for one thick tile: "+name)
        elif len(name) == 2:
            if name[1] == "t": # Upper
                y = 0
            elif name[1] == "c":
                y = 1
            elif name[1] == "l": # Lower
                y = 2
            else:
                raise AttributeError("Invalid attribute for three thick tile: "+name)
            if name[0] == "l": # Left
                x = 3
            elif name[0] == "c": # Center 
                x = 4
            elif name[0] == "r": # Right
                x = 5
            else:
                raise AttributeError("Invalid attribute for three thick tile: "+name)
            return tile2rect((x, y))
    
class Player:
    class Walk:
        frames = (0, 2, 0, 3)
        class Right:
            def __getitem__(self, index):
                if index in range(4):
                    return tile2rect((6, Walk.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        class Left:
            def __getitem__(self, index):
                if index in range(4):
                    return tile2rect((7, Walk.frames[index]))
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
                    return tile2rect((6, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
                
        class Left:
            def __getitem__(self, index):
                if index in range(2):
                    return tile2rect((7, Stand.frames[index]))
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
                    return tile2rect((6, Stand.frames[index]))
                else:
                    raise IndexError("Invalid frame index")
        class Left:
            def __getitem__(self, index):
                if index in range(5):
                    return tile2rect((7, Stand.frames[index]))
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
            return tile2rect((3, 3+index))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class Checkpoint:
    def __getitem__(self, index):
        if index in (0, 1, 2):
            return tile2rect((index, 4), (1, 2))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class Seed:
    def __getitem__(self, index):
        if index in (0, 1, 2):
            return tile2rect((index, 3))
        else:
            raise IndexError("Invalid sprite reference, not in 0-2")
    
class Sheet:
    def __init__(self):
        self.player = Player()
        self.platform = Platform()
        self.end = End()
        self.seed = Seed()
        self.checkpoint = Checkpoint()
        
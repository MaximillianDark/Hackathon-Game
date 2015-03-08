"""Sprite module for the project."""
    
import src.gfx

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
            
    def __str__(self):
        return str(self.spritelist)
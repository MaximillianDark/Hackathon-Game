"""Tile class."""

from src.sprite import Sprite

class Tile(Sprite):
    def __init__(self, sheet, src, dest, groups=None):
        self.sheet = sheet
        self.src = getattr(sheet.platform, src)
        self.dest = dest
        if groups:
            for g in groups:
                g.add(self)
    
    def update(self, *args):
        pass
    
    def render(self, renderer):
        renderer.render(self.sheet.tex, self.src, self.dest)
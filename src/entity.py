"""Entity classes for the project."""

from src.gfx import Rect
from src.sprite import Sprite

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
        
    def __sub__(self, other):
        return self + -other
        
    def __mul__(self, other):
        if isinstance(other, (Integer, Double)):
            return Vector(self.x*other, self.y*other)
        elif isinstance(other, Vector):
            return self.x*other.x+self.y*other.y
        else:
            raise NotImplementedError("Unusable type passed to Vector.__mul__")
        

class Entity(Sprite):
    def __init__(self, src, dest, groups=None):
        super(Entity, self).__init__(src, dest, groups)
        self.vec = Vector(0, 0)
        self.state = None # useful for subclasses
        
class Seed(Entity):
    frames = (0, 1, 0, 2)
    def __init__(self, pos, sheet, groups=None):
        self.sheet = sheet
        src = self.sheet.seed[0]
        super(Seed, self).__init__(src, Rect(pos[0], pos[1], src.w, src.h), groups)
        self.state = 0
    def update(self, *args):
        self.state += 1
        self.state %= len(Seed.frames)
        self.src = self.sheet.seed[Seed.frames[self.state]]
        
    def render(self, renderer):
        renderer.render(self.sheet.tex, self.src, self.dest)
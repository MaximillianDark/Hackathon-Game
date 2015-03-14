"""Entity classes for the project."""

from src.gfx import Rect
from src.sprite import Sprite, Group

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
    def __init__(self, sheet, pos, groups=None):
        self.sheet = sheet
        src = self.sheet.seed[0]
        super(Seed, self).__init__(src, Rect(pos[0], pos[1], src.w, src.h), groups)
        self.state = 0
    def update(self, *args):
        self.state += 0.2
        self.state %= len(Seed.frames)
        self.src = self.sheet.seed[Seed.frames[int(self.state)]]
        
    def render(self, renderer):
        renderer.render(self.src, self.dest)
        
class End(Entity):
    """Endpoint of a level."""
    frames = (0, 1, 2, 1)
    def __init__(self, sheet, pos, groups=None):
        self.sheet = sheet
        src = self.sheet.end[0]
        super(End, self).__init__(src, Rect(pos[0], pos[1], src.w, src.h), groups)
        self.state = 0
    def update(self, *args):
        self.state += 0.3
        self.state %= len(End.frames)
        self.src = self.sheet.end[End.frames[int(self.state)]]
    def render(self, renderer):
        renderer.render(self.src, self.dest)
        
class Player(Entity):
    pass
        
        
class Checkpoint(Entity):
    """Checkpoint in a level to save player progress."""
    frames = (0, 1, 2)
    def __init__(self, sheet, pos, groups=None):
        self.sheet = sheet
        src = self.sheet.checkpoint[0]
        super(Checkpoint, self).__init__(src, Rect(pos[0], pos[1], src.w, src.h), groups)
        self.state = 0
        
    def update(self, *args):
        if self.state > 0 and self.state < 2:
            self.state += 0.2
        elif args and args[0] and isinstance(args[0], Group):
            interactables = args[0]
            for other in interactables.collide_with(self):
                if isinstance(other, Player):
                    self.state = 0.2 # start transition
                    # would notify game of checkpoint here
        else:
            pass
        self.src = self.sheet.checkpoint[Checkpoint.frames[int(self.state)]]
        
    def render(self, renderer):
        renderer.render(self.src, self.dest)
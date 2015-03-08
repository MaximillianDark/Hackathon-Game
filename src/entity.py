"""Entity classes for the project."""

from sprite import Sprite

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
        
    def __sub__(self, other):
        return 
        

class Entity(Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.vec = Vector(0, 0)
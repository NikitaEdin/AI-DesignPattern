import math

class Target():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
class Adapter():
    def __init__(self, target):
        self.target = target
    
    def get_position(self):
        return self.target.get_position()
    
    def move(self, dx, dy):
        self.target.move(dx, dy)
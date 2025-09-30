import copy

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def __str__(self):
        return f"Circle({self.x}, {self.y}, {self.radius})"

if __name__ == "__main__":
    original = Circle(10, 20, 5)
    duplicate = original.clone()
    print(original)
    print(duplicate)
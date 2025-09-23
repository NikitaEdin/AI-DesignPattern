import copy

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.__class__.__name__}(color={self.color}, x={self.x}, y={self.y})"

class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius

if __name__ == "__main__":
    original = Circle("red", 10, 20, 5)
    cloned = original.clone()
    cloned.color = "blue"
    cloned.x = 30
    
    print(original)
    print(cloned)
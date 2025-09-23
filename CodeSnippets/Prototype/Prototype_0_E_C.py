import copy

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.color} shape at ({self.x}, {self.y})"

class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius
    
    def __str__(self):
        return f"{self.color} circle at ({self.x}, {self.y}) radius {self.radius}"

if __name__ == "__main__":
    original = Circle("red", 10, 20, 5)
    cloned = original.clone()
    cloned.color = "blue"
    cloned.x = 30
    
    print(original)
    print(cloned)
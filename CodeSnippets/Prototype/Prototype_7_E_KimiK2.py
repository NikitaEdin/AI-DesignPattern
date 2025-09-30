import copy

class Shape:
    def __init__(self, color, size):
        self.color = color
        self.size = size
    
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, color, size, radius):
        super().__init__(color, size)
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, color, size, width, height):
        super().__init__(color, size)
        self.width = width
        self.height = height

if __name__ == "__main__":
    original = Circle("red", 10, 5)
    copy1 = original.clone()
    copy1.color = "blue"
    
    print(original.color, original.radius)
    print(copy1.color, copy1.radius)
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
        return f"Circle at ({self.x}, {self.y}) with radius {self.radius}"

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle at ({self.x}, {self.y}) with size {self.width}x{self.height}"

if __name__ == "__main__":
    original_circle = Circle(10, 20, 5)
    cloned_circle = original_circle.clone()
    cloned_circle.x = 30
    print(original_circle)
    print(cloned_circle)

    original_rect = Rectangle(5, 5, 15, 25)
    cloned_rect = original_rect.clone()
    cloned_rect.width = 50
    print(original_rect)
    print(cloned_rect)
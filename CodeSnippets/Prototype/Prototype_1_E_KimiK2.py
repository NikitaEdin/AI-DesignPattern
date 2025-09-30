import copy

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        self.radius = radius
    
    def __str__(self):
        return f"Circle({self.x}, {self.y}, {self.color}, {self.radius})"

class Rectangle(Shape):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"Rectangle({self.x}, {self.y}, {self.color}, {self.width}, {self.height})"

if __name__ == "__main__":
    original_circle = Circle(10, 20, "red", 5)
    cloned_circle = original_circle.clone()
    cloned_circle.x = 30
    
    original_rect = Rectangle(0, 0, "blue", 10, 20)
    cloned_rect = original_rect.clone()
    cloned_rect.color = "green"
    
    print(original_circle)
    print(cloned_circle)
    print(original_rect)
    print(cloned_rect)
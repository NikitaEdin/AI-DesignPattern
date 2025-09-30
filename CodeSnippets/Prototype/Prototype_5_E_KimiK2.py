import copy

class Shape:
    def __init__(self, color):
        self.color = color
    
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
    
    def __str__(self):
        return f"Circle({self.color}, {self.radius})"

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"Rectangle({self.color}, {self.width}, {self.height})"

if __name__ == "__main__":
    original_circle = Circle("red", 10)
    cloned_circle = original_circle.clone()
    cloned_circle.color = "blue"
    
    original_rect = Rectangle("green", 5, 8)
    cloned_rect = original_rect.clone()
    cloned_rect.width = 15
    
    print(original_circle)
    print(cloned_circle)
    print(original_rect)
    print(cloned_rect)
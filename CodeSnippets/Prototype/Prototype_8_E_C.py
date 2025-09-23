import copy

class Shape:
    def __init__(self, color):
        self.color = color
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.__class__.__name__} with color {self.color}"

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

if __name__ == "__main__":
    original_circle = Circle("red", 5)
    cloned_circle = original_circle.clone()
    
    original_rect = Rectangle("blue", 10, 20)
    cloned_rect = original_rect.clone()
    
    print(original_circle)
    print(cloned_circle)
    print(original_rect)
    print(cloned_rect)
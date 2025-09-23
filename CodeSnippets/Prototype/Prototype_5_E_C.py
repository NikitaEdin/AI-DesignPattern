import copy

class Shape:
    def __init__(self, color):
        self.color = color
    
    def clone(self):
        return copy.deepcopy(self)
    
    def draw(self):
        print(f"Drawing {self.__class__.__name__} in {self.color}")

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
    cloned_circle.color = "blue"
    
    original_circle.draw()
    cloned_circle.draw()
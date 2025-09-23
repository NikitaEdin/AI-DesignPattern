class Shape:
    def __init__(self, color):
        self.color = color
    
    def draw(self):
        print(f"Drawing a {self.color} shape")
    
    def clone(self):
        return self.__class__(self.color)

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def draw(self):
        print(f"Drawing a {self.color} rectangle with width {self.width} and height {self.height}")

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
    
    def draw(self):
        print(f"Drawing a {self.color} circle with radius {self.radius}")

def main():
    rectangle1 = Rectangle("red", 5, 7)
    rectangle2 = rectangle1.clone()
    rectangle2.width = 10
    rectangle2.height = 14
    
    print(rectangle1.color)
    rectangle1.draw()
    print(rectangle2.color)
    rectangle2.draw()
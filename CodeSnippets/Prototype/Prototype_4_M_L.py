class Shape:
    def __init__(self, color):
        self.color = color

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height, color):
        super().__init__(color)
        self.base = base
        self.height = height

    def set_base(self, base):
        self.base = base

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return 0.5 * self.base * self.height

def main():
    # Create a circle
    circle = Circle(3, "red")
    print(circle.get_color()) # prints "red"
    circle.set_color("blue")
    print(circle.get_color()) # prints "blue"

    # Create a rectangle
    rectangle = Rectangle(5, 7, "green")
    print(rectangle.get_area()) # prints 35
    rectangle.set_width(10)
    print(rectangle.get_area()) # prints 70

    # Create a triangle
    triangle = Triangle(6, 9, "red")
    print(triangle.get_area()) # prints 27
    triangle.set_base(4)
    print(triangle.get_area()) # prints 18
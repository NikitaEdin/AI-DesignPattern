import math

class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height

class ShapeCreator:
    @staticmethod
    def create(shape_type, *args):
        if shape_type == "circle":
            if len(args) != 1 or args[0] <= 0:
                raise ValueError("Circle requires positive radius")
            return Circle(*args)
        elif shape_type == "rectangle":
            if len(args) != 2 or any(a <= 0 for a in args):
                raise ValueError("Rectangle requires positive width and height")
            return Rectangle(*args)
        else:
            raise ValueError("Unknown shape type")

if __name__ == "__main__":
    shapes = [
        ShapeCreator.create("circle", 5),
        ShapeCreator.create("rectangle", 4, 6),
    ]
    for s in shapes:
        print(round(s.area(), 2))
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class ShapeCreator:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle(5)
        elif shape_type == "square":
            return Square(4)
        return None

if __name__ == "__main__":
    creator = ShapeCreator()
    circle = creator.create_shape("circle")
    square = creator.create_shape("square")
    print(circle.area())
    print(square.area())
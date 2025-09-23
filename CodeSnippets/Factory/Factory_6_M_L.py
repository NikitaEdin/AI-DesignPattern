class Shape:
    def draw(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self):
        print("Drawing a rectangle with width {}, and height {}".format(self.width, self.height))

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        print("Drawing a circle with radius {}".format(self.radius))

def create_shape(name, width=None, height=None, radius=None):
    if name == "Rectangle":
        return Rectangle(width, height)
    elif name == "Circle":
        return Circle(radius)
    else:
        raise ValueError("Invalid shape name")

if __name__ == "__main__":
    rectangle = create_shape("Rectangle", 10, 5)
    rectangle.draw()

    circle = create_shape("Circle", radius=3)
    circle.draw()
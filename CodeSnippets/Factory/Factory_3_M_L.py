class ShapeFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_shape(name, *args, **kwargs):
        if name == "circle":
            return Circle(*args, **kwargs)
        elif name == "square":
            return Square(*args, **kwargs)
        elif name == "triangle":
            return Triangle(*args, **kwargs)
        else:
            raise ValueError(f"Invalid shape: {name}")

class Shape:
    def __init__(self, color):
        self.color = color

class Circle(Shape):
    def __init__(self, radius, color="red"):
        super().__init__(color)
        self.radius = radius

class Square(Shape):
    def __init__(self, side_length, color="blue"):
        super().__init__(color)
        self.side_length = side_length

class Triangle(Shape):
    def __init__(self, base, height, color="green"):
        super().__init__(color)
        self.base = base
        self.height = height

if __name__ == "__main__":
    factory = ShapeFactory()

    circle1 = factory.create_shape("circle", 5)
    print(circle1.radius)

    square2 = factory.create_shape("square", 6)
    print(square2.side_length)

    triangle3 = factory.create_shape("triangle", 7, 8)
    print(triangle3.base, triangle3.height)
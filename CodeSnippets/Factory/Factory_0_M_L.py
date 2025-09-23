class ShapeFactory:
    @staticmethod
    def create_shape(name, **kwargs):
        if name == "square":
            return Square(**kwargs)
        elif name == "circle":
            return Circle(**kwargs)
        else:
            raise ValueError("Unsupported shape")

class Shape:
    def __init__(self, color="blue"):
        self.color = color

    def draw(self):
        print(f"Drawing {self.__class__.__name__} in {self.color}")

class Square(Shape):
    def __init__(self, size=10, color="blue"):
        super().__init__(color)
        self.size = size

    def draw(self):
        print(f"Drawing {self.__class__.__name__} with side length {self.size} in {self.color}")

class Circle(Shape):
    def __init__(self, radius=10, color="blue"):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        print(f"Drawing {self.__class__.__name__} with radius {self.radius} in {self.color}")

def main():
    shape_factory = ShapeFactory()
    square = shape_factory.create_shape("square", size=10)
    circle = shape_factory.create_shape("circle", radius=5)

    square.draw()
    circle.draw()

if __name__ == "__main__":
    main()
class ShapeFactory:
    @staticmethod
    def get_shape(name):
        if name == "square":
            return Square()
        elif name == "circle":
            return Circle()
        else:
            raise ValueError("Invalid shape")

class Shape:
    def __init__(self, color):
        self.color = color

    def draw(self):
        print(f"Drawing {self.color} shape")

class Square(Shape):
    def __init__(self, color="red"):
        super().__init__(color)

    def draw(self):
        print(f"Drawing {self.color} square")

class Circle(Shape):
    def __init__(self, color="blue"):
        super().__init__(color)

    def draw(self):
        print(f"Drawing {self.color} circle")

def main():
    shape_factory = ShapeFactory()
    square = shape_factory.get_shape("square")
    circle = shape_factory.get_shape("circle")

    square.draw()
    circle.draw()

if __name__ == "__main__":
    main()
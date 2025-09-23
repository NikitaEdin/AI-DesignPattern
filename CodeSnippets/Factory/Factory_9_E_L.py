class Product:
    def __init__(self, name: str) -> None:
        self.name = name

class ShapeFactory:
    @staticmethod
    def create_shape(name: str) -> Product:
        if name == "circle":
            return Circle()
        elif name == "square":
            return Square()
        else:
            raise ValueError("Invalid shape name")

class Circle(Product):
    def __init__(self, radius=1.0) -> None:
        super().__init__("circle")
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius ** 2

class Square(Product):
    def __init__(self, side_length=1.0) -> None:
        super().__init__("square")
        self.side_length = side_length

    def area(self) -> float:
        return self.side_length ** 2

if __name__ == "__main__":
    circle = ShapeFactory.create_shape("circle")
    print(f"Circle area: {circle.area()}")

    square = ShapeFactory.create_shape("square")
    print(f"Square area: {square.area()}")
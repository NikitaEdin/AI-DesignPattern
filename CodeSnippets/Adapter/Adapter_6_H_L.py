class Shape:
    def __init__(self, color):
        self.color = color

    def draw(self):
        print("Drawing a shape.")

class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        print("Drawing a circle.")
        print(f"Circle with radius {self.radius} and color {self.color}.")

class Rectangle:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        print("Drawing a rectangle.")
        print(f"Rectangle with dimensions {self.width}x{self.height} and color {self.color}.")

class Triangle:
    def __init__(self, base, height, color):
        self.base = base
        self.height = height
        self.color = color

    def draw(self):
        print("Drawing a triangle.")
        print(f"Triangle with base {self.base} and height {self.height} and color {self.color}.")

class ShapeAdapter:
    def __init__(self, shape):
        self.shape = shape

    def draw(self):
        if isinstance(self.shape, Circle):
            radius = self.shape.radius
            print("Drawing a circle.")
            print(f"Circle with radius {radius} and color {self.shape.color}.")
        elif isinstance(self.shape, Rectangle):
            width = self.shape.width
            height = self.shape.height
            print("Drawing a rectangle.")
            print(f"Rectangle with dimensions {width}x{height} and color {self.shape.color}.")
        elif isinstance(self.shape, Triangle):
            base = self.shape.base
            height = self.shape.height
            print("Drawing a triangle.")
            print(f"Triangle with base {base} and height {height} and color {self.shape.color}.")
        else:
            raise ValueError("Unsupported shape type.")

def main():
    circle = Circle(5, "red")
    rectangle = Rectangle(3, 4, "blue")
    triangle = Triangle(6, 7, "green")

    adapter1 = ShapeAdapter(circle)
    adapter2 = ShapeAdapter(rectangle)
    adapter3 = ShapeAdapter(triangle)

    adapter1.draw()
    adapter2.draw()
    adapter3.draw()

if __name__ == "__main__":
    main()
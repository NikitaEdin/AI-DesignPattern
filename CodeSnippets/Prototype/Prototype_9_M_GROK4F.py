class Shape:
    def __init__(self, color, position):
        if not isinstance(color, str):
            raise ValueError("Color must be a string")
        self.color = color
        self.position = position

    def draw(self):
        pass

    def replicate(self):
        raise NotImplementedError("Subclasses must implement replicate")

class Circle(Shape):
    def __init__(self, color, position, radius):
        super().__init__(color, position)
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number")
        self.radius = radius

    def draw(self):
        print(f"Drawing circle of radius {self.radius} in {self.color} at {self.position}")

    def replicate(self):
        return Circle(self.color, self.position, self.radius)

class Rectangle(Shape):
    def __init__(self, color, position, width, height):
        super().__init__(color, position)
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number")
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive number")
        self.width = width
        self.height = height

    def draw(self):
        print(f"Drawing rectangle {self.width}x{self.height} in {self.color} at {self.position}")

    def replicate(self):
        return Rectangle(self.color, self.position, self.width, self.height)

if __name__ == "__main__":
    original_circle = Circle("red", (10, 20), 5)
    cloned_circle = original_circle.replicate()
    cloned_circle.color = "blue"
    cloned_circle.radius = 10

    original_circle.draw()
    cloned_circle.draw()

    original_rectangle = Rectangle("green", (30, 40), 15, 25)
    cloned_rectangle = original_rectangle.replicate()
    cloned_rectangle.color = "yellow"
    cloned_rectangle.width = 20

    original_rectangle.draw()
    cloned_rectangle.draw()
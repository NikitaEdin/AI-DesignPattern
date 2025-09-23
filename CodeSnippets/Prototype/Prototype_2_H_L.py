class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        print(f"Drawing shape at {self.x}, {self.y}")

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self):
        print(f"Drawing circle at {self.x}, {self.y} with radius {self.radius}")

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def draw(self):
        print(f"Drawing rectangle at {self.x}, {self.y} with size {self.width} x {self.height}")

class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.vertices = [(x1, y1), (x2, y2), (x3, y3)]

    def draw(self):
        print(f"Drawing triangle with vertices: {', '.join([str(v) for v in self.vertices])}")

def main():
    shapes = []

    # Create some shapes and add them to the list
    shapes.append(Circle(1, 2, 3))
    shapes.append(Rectangle(4, 5, 6, 7))
    shapes.append(Triangle(8, 9, 10, 11, 12, 13))

    # Move all the shapes to a new position
    for shape in shapes:
        shape.move(10, 10)

    # Draw all the shapes
    for shape in shapes:
        shape.draw()
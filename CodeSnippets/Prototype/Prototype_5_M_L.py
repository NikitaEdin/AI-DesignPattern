# Prototype Design Pattern Implementation in Python

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def clone(self):
        return Shape(self.color, self.x, self.y)

class Circle(Shape):
    def __init__(self, radius, color, x, y):
        super().__init__(color, x, y)
        self.radius = radius

    def clone(self):
        return Circle(self.radius, self.color, self.x, self.y)

class Rectangle(Shape):
    def __init__(self, width, height, color, x, y):
        super().__init__(color, x, y)
        self.width = width
        self.height = height

    def clone(self):
        return Rectangle(self.width, self.height, self.color, self.x, self.y)

def main():
    # Create two instances of the Circle and Rectangle classes
    circle1 = Circle(5, "red", 10, 20)
    rectangle1 = Rectangle(10, 5, "blue", 30, 40)

    # Clone the shapes
    circle2 = circle1.clone()
    rectangle2 = rectangle1.clone()

    # Print the original shapes and their clones
    print("Original Circle:")
    print(circle1)
    print("Cloned Circle:")
    print(circle2)
    print("\nOriginal Rectangle:")
    print(rectangle1)
    print("Cloned Rectangle:")
    print(rectangle2)
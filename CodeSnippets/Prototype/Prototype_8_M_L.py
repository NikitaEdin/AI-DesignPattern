# Prototype Design Pattern Implementation in Python

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        print("Drawing a shape with color", self.color)

    def clone(self):
        return Shape(self.color, self.x, self.y)

class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(radius, x, y)
        self.radius = radius

    def draw(self):
        print("Drawing a circle with radius", self.radius)

    def clone(self):
        return Circle(self.radius, self.x, self.y)

class Rectangle(Shape):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y)
        self.width = width
        self.height = height

    def draw(self):
        print("Drawing a rectangle with dimensions", self.width, self.height)

    def clone(self):
        return Rectangle(self.width, self.height, self.x, self.y)

# Usage Example
def main():
    circle1 = Circle(5, 10, 20)
    circle2 = circle1.clone()
    rectangle1 = Rectangle(10, 5, 30, 40)

    print("Shape:", circle1)
    print("Color:", circle1.color)
    print("X:", circle1.x)
    print("Y:", circle1.y)
    print("Radius:", circle1.radius)
    print("\n")

    print("Shape:", circle2)
    print("Color:", circle2.color)
    print("X:", circle2.x)
    print("Y:", circle2.y)
    print("Radius:", circle2.radius)
    print("\n")

    print("Shape:", rectangle1)
    print("Color:", rectangle1.color)
    print("X:", rectangle1.x)
    print("Y:", rectangle1.y)
    print("Width:", rectangle1.width)
    print("Height:", rectangle1.height)

if __name__ == "__main__":
    main()
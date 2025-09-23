python
class Shape:
    def __init__(self, color):
        self.color = color

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

def main():
    circle1 = Circle("red", 5)
    print(circle1.color) # prints "red"
    print(circle1.radius) # prints 5

    rectangle1 = Rectangle("blue", 10, 20)
    print(rectangle1.color) # prints "blue"
    print(rectangle1.width) # prints 10
    print(rectangle1.height) # prints 20

if __name__ == "__main__":
    main()

```
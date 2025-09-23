```python
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

class ShapeAdapter:
    def __init__(self, shape):
        self.shape = shape

    def area(self):
        if isinstance(self.shape, Circle):
            return math.pi * self.shape.radius ** 2
        elif isinstance(self.shape, Rectangle):
            return self.shape.width * self.shape.height
        elif isinstance(self.shape, Triangle):
            return 0.5 * self.shape.base * self.shape.height
        else:
            raise ValueError("Unsupported shape")

def main():
    circle = Circle(5)
    rectangle = Rectangle(10, 20)
    triangle = Triangle(10, 20)

    print(ShapeAdapter(circle).area()) # Output: 78.5
    print(ShapeAdapter(rectangle).area()) # Output: 200
    print(ShapeAdapter(triangle).area()) # Output: 50

if __name__ == "__main__":
    main()
    ```
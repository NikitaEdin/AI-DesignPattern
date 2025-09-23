import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return (self.base * self.height) / 2

class AdapterCircleToTriangle:
    def __init__(self, circle):
        self.circle = circle

    def get_area(self):
        return self.circle.area() * 2

if __name__ == "__main__":
    c = Circle(3)
    t = AdapterCircleToTriangle(c)
    print("The area of the triangle is:", t.get_area())
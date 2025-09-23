class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

class CircleCloner:
    def clone(self, circle, radius):
        new_circle = Circle(radius)
        new_circle.area = circle.area()
        return new_circle
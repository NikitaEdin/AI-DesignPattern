class ShapeFactory:
    def __init__(self):
        self.shapes = {}

    def register(self, name, shape_class):
        self.shapes[name] = shape_class

    def create(self, name, *args, **kwargs):
        return self.shapes[name](*args, **kwargs)

class Circle:
    def __init__(self, radius):
        self.radius = radius

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

# Example usage
factory = ShapeFactory()
factory.register("circle", Circle)
factory.register("rectangle", Rectangle)

circle = factory.create("circle", 5)
print(circle.radius) # Output: 5

rectangle = factory.create("rectangle", 10, 20)
print(rectangle.width, rectangle.height) # Output: 10 20
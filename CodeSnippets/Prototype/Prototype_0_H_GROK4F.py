class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def duplicate(self):
        return Point(self.x, self.y)

class Circle:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def duplicate(self):
        cloned_center = self.center.duplicate() if self.center else None
        return Circle(cloned_center, self.radius, self.color)

    def draw(self):
        print(f"Drawing {self.color} circle at ({self.center.x}, {self.center.y}) with radius {self.radius}")

class Rectangle:
    def __init__(self, position, width, height, color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color

    def duplicate(self):
        cloned_position = self.position.duplicate() if self.position else None
        return Rectangle(cloned_position, self.width, self.height, self.color)

    def draw(self):
        print(f"Drawing {self.color} rectangle at ({self.position.x}, {self.position.y}) size {self.width}x{self.height}")

class ShapeRegistry:
    def __init__(self):
        self._shapes = {}

    def register(self, name, shape):
        if name in self._shapes:
            raise ValueError(f"Shape with name '{name}' already registered")
        self._shapes[name] = shape

    def create_copy(self, name):
        if name not in self._shapes:
            raise ValueError(f"No shape registered with name '{name}'")
        prototype = self._shapes[name]
        return prototype.duplicate()

if __name__ == "__main__":
    registry = ShapeRegistry()

    center = Point(5, 10)
    circle_original = Circle(center, 3, "red")
    registry.register("basic_circle", circle_original)

    pos = Point(0, 0)
    rect_original = Rectangle(pos, 4, 6, "blue")
    registry.register("standard_rect", rect_original)

    cloned_circle = registry.create_copy("basic_circle")
    cloned_circle.center.x = 15
    cloned_circle.draw()

    circle_original.draw()

    cloned_rect = registry.create_copy("standard_rect")
    cloned_rect.position.y = 20
    cloned_rect.draw()

    rect_original.draw()

    try:
        invalid_copy = registry.create_copy("missing_shape")
    except ValueError as e:
        print(f"Error: {e}")
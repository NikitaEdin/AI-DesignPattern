class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def clone(self):
        raise NotImplementedError("Subclasses must implement clone")

class Circle(Shape):
    def __init__(self, x=0, y=0, radius=1):
        super().__init__(x, y)
        self.radius = radius

    def clone(self):
        return Circle(self.x, self.y, self.radius)

class Rectangle(Shape):
    def __init__(self, x=0, y=0, width=1, height=1):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def clone(self):
        return Rectangle(self.x, self.y, self.width, self.height)

class ShapeManager:
    def __init__(self):
        self._prototypes = {}

    def register(self, name, shape):
        if not isinstance(shape, Shape):
            raise ValueError("Registered item must be a Shape instance")
        self._prototypes[name] = shape

    def create_clone(self, name):
        if name not in self._prototypes:
            raise ValueError(f"Unknown shape name: {name}")
        return self._prototypes[name].clone()

if __name__ == "__main__":
    manager = ShapeManager()
    original_circle = Circle(10, 20, 5)
    manager.register("basic_circle", original_circle)
    original_rect = Rectangle(0, 0, 10, 5)
    manager.register("basic_rectangle", original_rect)
    cloned_circle = manager.create_clone("basic_circle")
    cloned_rect = manager.create_clone("basic_rectangle")
    print(f"Cloned circle: x={cloned_circle.x}, y={cloned_circle.y}, radius={cloned_circle.radius}")
    print(f"Cloned rectangle: x={cloned_rect.x}, y={cloned_rect.y}, width={cloned_rect.width}, height={cloned_rect.height}")
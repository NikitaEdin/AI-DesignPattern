class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def duplicate(self):
        if self is None:
            return None
        return Point(self.x, self.y)

class GraphicElement:
    def __init__(self, position=Point(), color="black"):
        self.position = position
        self.color = color

    def duplicate(self):
        new_instance = type(self)(self.position.duplicate(), self.color)
        new_instance.position = self.position.duplicate()
        return new_instance

class Circle(GraphicElement):
    def __init__(self, position=Point(), color="black", radius=1.0):
        super().__init__(position, color)
        self.radius = radius

    def duplicate(self):
        new_circle = super().duplicate()
        new_circle.radius = self.radius
        return new_circle

class Rectangle(GraphicElement):
    def __init__(self, position=Point(), color="black", width=1.0, height=1.0):
        super().__init__(position, color)
        self.width = width
        self.height = height

    def duplicate(self):
        new_rect = super().duplicate()
        new_rect.width = self.width
        new_rect.height = self.height
        return new_rect

class ElementRegistry:
    def __init__(self):
        self._elements = {}

    def register(self, name, element):
        if element is None:
            raise ValueError("Cannot register None element")
        if name in self._elements:
            raise ValueError(f"Element '{name}' already registered")
        self._elements[name] = element

    def create_duplicate(self, name, modifications=None):
        if name not in self._elements:
            raise ValueError(f"No element registered with name '{name}'")
        cloned = self._elements[name].duplicate()
        if modifications:
            for key, value in modifications.items():
                if hasattr(cloned, key):
                    setattr(cloned, key, value)
                else:
                    setattr(cloned.position, key, value) if key in ['x', 'y'] else None
        return cloned

    def unregister(self, name):
        if name in self._elements:
            del self._elements[name]

if __name__ == "__main__":
    registry = ElementRegistry()

    orig_point = Point(10, 20)
    orig_circle = Circle(orig_point, "red", 5.0)
    registry.register("basic_circle", orig_circle)

    orig_rect = Rectangle(Point(0, 0), "blue", 4.0, 6.0)
    registry.register("basic_rect", orig_rect)

    cloned_circle = registry.create_duplicate("basic_circle")
    print(f"Cloned circle position: ({cloned_circle.position.x}, {cloned_circle.position.y}), radius: {cloned_circle.radius}, color: {cloned_circle.color}")

    cloned_rect = registry.create_duplicate("basic_rect", modifications={"color": "green"})
    print(f"Cloned rect position: ({cloned_rect.position.x}, {cloned_rect.position.y}), width: {cloned_rect.width}, height: {cloned_rect.height}, color: {cloned_rect.color}")

    orig_point.x = 100
    print(f"After modifying original point, cloned circle position: ({cloned_circle.position.x}, {cloned_circle.position.y})")

    modified_clone = registry.create_duplicate("basic_circle", modifications={"radius": 10.0, "x": 50})
    print(f"Modified clone position: ({modified_clone.position.x}, {modified_clone.position.y}), radius: {modified_clone.radius}")

    registry.unregister("basic_circle")
    try:
        registry.create_duplicate("basic_circle")
    except ValueError as e:
        print(f"Edge case - unregistered: {e}")
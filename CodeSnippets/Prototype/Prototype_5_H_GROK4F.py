import abc
import copy

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

class Shape(abc.ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def duplicate(self):
        cloned = copy.deepcopy(self)
        # Handle edge case: ensure position is fully independent
        if hasattr(cloned, 'position') and cloned.position is not None:
            cloned.position = Position(cloned.position.x, cloned.position.y)
        return cloned

    @abc.abstractmethod
    def area(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.position} with {self.color}"

class Rectangle(Shape):
    def __init__(self, color, position, width, height):
        super().__init__(color, position)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __repr__(self):
        return f"{super().__repr__()} width={self.width} height={self.height}"

class Circle(Shape):
    def __init__(self, color, position, radius):
        super().__init__(color, position)
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def __repr__(self):
        return f"{super().__repr__()} radius={self.radius}"

class InstanceManager:
    def __init__(self):
        self._instances = {}

    def add(self, identifier, instance):
        if not isinstance(instance, Shape):
            raise ValueError("Only Shape instances can be added")
        self._instances[identifier] = instance

    def create_copy(self, identifier):
        if identifier not in self._instances:
            raise KeyError(f"No instance registered with identifier '{identifier}'")
        prototype = self._instances[identifier]
        # Advanced: Custom deep copy with validation
        copied = copy.deepcopy(prototype)
        if copied.color is prototype.color:
            raise RuntimeError("Shallow copy detected; deep copy failed")
        return copied

if __name__ == "__main__":
    # Create initial instances
    red_color = Color(255, 0, 0)
    origin = Position(0, 0)
    initial_rect = Rectangle(red_color, origin, 10, 20)
    initial_circle = Circle(red_color, origin, 5)

    # Direct duplication
    rect_copy = initial_rect.duplicate()
    rect_copy.position.x = 100
    rect_copy.color.r = 0
    rect_copy.width = 30
    print(f"Original rectangle: {initial_rect}")
    print(f"Duplicated rectangle: {rect_copy}")
    print(f"Original area unchanged: {initial_rect.area() == 200}")
    print(f"Color deep copied: {initial_rect.color.r == 255}")

    # Manager usage
    manager = InstanceManager()
    manager.add("default_rect", initial_rect)
    manager.add("default_circle", initial_circle)

    new_rect = manager.create_copy("default_rect")
    new_circle = manager.create_copy("default_circle")
    new_rect.position.y = 50
    new_circle.radius = 10
    new_circle.color.b = 255

    print(f"\nManager-created rectangle: {new_rect}")
    print(f"Manager-created circle: {new_circle}")
    print(f"Original circle unchanged: {initial_circle.radius == 5 and initial_circle.color.b == 0}")
    print(f"Manager copy validation passed")
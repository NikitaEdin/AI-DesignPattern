from abc import ABC, abstractmethod
from copy import deepcopy
import uuid

class Shape(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())

    @abstractmethod
    def copy(self):
        pass

    def __str__(self):
        return f"Shape(id={self.id})"

class Circle(Shape):
    def __init__(self, radius=1.0):
        super().__init__()
        self.radius = radius

    def copy(self):
        return Circle(self.radius)

    def __str__(self):
        return f"Circle(id={self.id}, radius={self.radius})"

class Rectangle(Shape):
    def __init__(self, width=1.0, height=1.0):
        super().__init__()
        self.width = width
        self.height = height

    def copy(self):
        return Rectangle(self.width, self.height)

    def __str__(self):
        return f"Rectangle(id={self.id}, width={self.width}, height={self.height})"

class CompositeShape(Shape):
    def __init__(self):
        super().__init__()
        self.components = []

    def add(self, shape):
        if not isinstance(shape, Shape):
            raise ValueError("Only Shape instances can be added")
        self.components.append(shape)

    def copy(self):
        cloned = CompositeShape()
        for component in self.components:
            cloned.add(component.copy())
        return cloned

    def __str__(self):
        return f"CompositeShape(id={self.id}, components={len(self.components)})"

class ShapeManager:
    def __init__(self):
        self._registered = {}

    def register(self, name, shape):
        if not isinstance(shape, Shape):
            raise ValueError("Only Shape instances can be registered")
        self._registered[name] = shape

    def create_copy(self, name):
        if name not in self._registered:
            raise KeyError(f"No registered shape with name '{name}'")
        return self._registered[name].copy()

def main():
    manager = ShapeManager()

    # Register simple shapes
    circle = Circle(5.0)
    manager.register("basic_circle", circle)
    rect = Rectangle(3.0, 4.0)
    manager.register("basic_rect", rect)

    # Create clones
    cloned_circle = manager.create_copy("basic_circle")
    cloned_rect = manager.create_copy("basic_rect")

    # Modify clones independently
    cloned_circle.radius = 10.0
    print(f"Original circle: {circle}")
    print(f"Cloned circle: {cloned_circle}")

    # Composite example
    composite = CompositeShape()
    composite.add(circle)
    composite.add(rect)
    manager.register("basic_composite", composite)

    cloned_composite = manager.create_copy("basic_composite")
    cloned_composite.add(cloned_circle)  # Add to clone

    print(f"Original composite components: {len(composite.components)}")
    print(f"Cloned composite components: {len(cloned_composite.components)}")

    # Edge case: Unregistered
    try:
        manager.create_copy("nonexistent")
    except KeyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
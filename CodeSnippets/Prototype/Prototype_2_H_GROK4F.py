import copy
from abc import ABC, abstractmethod
from typing import List

class VisualElement(ABC):
    @abstractmethod
    def duplicate(self) -> 'VisualElement':
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

class Shape(VisualElement):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black"):
        self.x = x
        self.y = y
        self.color = color

    def duplicate(self) -> 'Shape':
        return copy.deepcopy(self)

    def draw(self) -> None:
        print(f"Drawing shape at ({self.x}, {self.y}) in {self.color}")

class Circle(Shape):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black", radius: int = 1):
        super().__init__(x, y, color)
        self.radius = radius

    def duplicate(self) -> 'Circle':
        new_instance = Circle(self.x, self.y, self.color, self.radius)
        return new_instance

    def draw(self) -> None:
        print(f"Drawing circle at ({self.x}, {self.y}) with radius {self.radius} in {self.color}")

class Rectangle(Shape):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black", width: int = 1, height: int = 1):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def duplicate(self) -> 'Rectangle':
        new_instance = Rectangle(self.x, self.y, self.color, self.width, self.height)
        return new_instance

    def draw(self) -> None:
        print(f"Drawing rectangle at ({self.x}, {self.y}) {self.width}x{self.height} in {self.color}")

class Container(VisualElement):
    def __init__(self, x: int = 0, y: int = 0, color: str = "gray"):
        self.x = x
        self.y = y
        self.color = color
        self.children: List[VisualElement] = []

    def add(self, element: VisualElement) -> None:
        if element is not None:
            self.children.append(element)
        else:
            raise ValueError("Cannot add None element")

    def duplicate(self) -> 'Container':
        new_container = Container(self.x, self.y, self.color)
        for child in self.children:
            if hasattr(child, 'duplicate'):
                cloned_child = child.duplicate()
                new_container.add(cloned_child)
            else:
                new_container.add(copy.deepcopy(child))
        return new_container

    def draw(self) -> None:
        print(f"Drawing container at ({self.x}, {self.y}) in {self.color}")
        for child in self.children:
            child.draw()

class ElementManager:
    def __init__(self):
        self._base_elements: dict[str, VisualElement] = {}

    def register(self, key: str, element: VisualElement) -> None:
        if key in self._base_elements:
            raise ValueError(f"Key {key} already registered")
        self._base_elements[key] = element

    def instantiate(self, key: str, **kwargs) -> VisualElement:
        if key not in self._base_elements:
            raise KeyError(f"No base element registered for {key}")
        base = self._base_elements[key]
        clone = base.duplicate()
        # Apply modifications if provided
        for attr, value in kwargs.items():
            if hasattr(clone, attr):
                setattr(clone, attr, value)
            if isinstance(clone, Container) and attr == 'children':
                # Handle adding new children to container
                if isinstance(value, list):
                    for child in value:
                        if child is not None:
                            clone.add(child)
        return clone

    def get_keys(self) -> list[str]:
        return list(self._base_elements.keys())

if __name__ == "__main__":
    manager = ElementManager()

    # Register base elements
    base_circle = Circle(10, 20, "red", 5)
    manager.register("circle", base_circle)

    base_rect = Rectangle(30, 40, "blue", 10, 15)
    manager.register("rect", base_rect)

    # Create a container with children
    panel = Container(0, 0, "gray")
    panel.add(Circle(5, 5, "green", 2))
    panel.add(Rectangle(10, 10, "yellow", 8, 6))
    manager.register("panel", panel)

    # Instantiate clones
    cloned_circle = manager.instantiate("circle", radius=7)
    cloned_circle.draw()

    cloned_rect = manager.instantiate("rect", color="purple", width=20)
    cloned_rect.draw()

    cloned_panel = manager.instantiate("panel")
    cloned_panel.add(Rectangle(15, 15, "orange", 4, 4))  # Add extra to clone
    cloned_panel.draw()

    print(f"Registered keys: {manager.get_keys()}")
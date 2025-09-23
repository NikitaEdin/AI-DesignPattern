import copy
from abc import ABC, abstractmethod

class GraphicItem(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def duplicate(self):
        pass

class Circle(GraphicItem):
    def __init__(self, name, radius, metadata=None):
        super().__init__(name)
        self.radius = radius
        self.metadata = metadata or {}

    def duplicate(self):
        try:
            return copy.deepcopy(self)
        except Exception as exc:
            raise RuntimeError("Failed to duplicate item") from exc

class Rectangle(GraphicItem):
    def __init__(self, name, width, height, metadata=None):
        super().__init__(name)
        self.width = width
        self.height = height
        self.metadata = metadata or {}

    def duplicate(self):
        return copy.deepcopy(self)

class TemplateManager:
    def __init__(self):
        self._store = {}

    def register(self, key, item):
        if not isinstance(item, GraphicItem):
            raise TypeError("Only GraphicItem instances can be registered")
        self._store[key] = item

    def create(self, key):
        try:
            template = self._store[key]
        except KeyError:
            raise KeyError(f"No template found for key: {key}")
        return template.duplicate()

if __name__ == "__main__":
    manager = TemplateManager()
    base_circle = Circle("base_circle", 5, metadata={"color": "red", "tags": ["unit"]})
    base_rect = Rectangle("panel", 200, 100, metadata={"color": "blue"})
    manager.register("circle_small", base_circle)
    manager.register("panel_large", base_rect)

    copy1 = manager.create("circle_small")
    copy1.name = "circle_copy_1"
    copy1.metadata["color"] = "green"

    copy2 = manager.create("panel_large")
    copy2.width = 300

    print(base_circle.name, base_circle.radius, base_circle.metadata)
    print(copy1.name, copy1.radius, copy1.metadata)
    print(base_rect.name, base_rect.width, base_rect.height, base_rect.metadata)
    print(copy2.name, copy2.width, copy2.height, copy2.metadata)
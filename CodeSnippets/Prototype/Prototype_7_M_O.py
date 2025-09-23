import copy
from typing import Dict, Any

class Copyable:
    def clone(self, **overrides):
        try:
            obj = copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError("Failed to duplicate object") from e
        for key, value in overrides.items():
            if not hasattr(obj, key):
                raise AttributeError(f"Attribute '{key}' not found on object")
            setattr(obj, key, value)
        return obj

class Circle(Copyable):
    def __init__(self, radius: float, color: str):
        self.radius = radius
        self.color = color
    def area(self):
        return 3.14159 * self.radius * self.radius
    def __repr__(self):
        return f"Circle(radius={self.radius}, color='{self.color}')"

class Rectangle(Copyable):
    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color = color
    def area(self):
        return self.width * self.height
    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height}, color='{self.color}')"

class TemplateStore:
    def __init__(self):
        self._store: Dict[str, Copyable] = {}
    def register(self, key: str, template: Copyable):
        if key in self._store:
            raise KeyError(f"Key '{key}' already registered")
        self._store[key] = template
    def unregister(self, key: str):
        if key not in self._store:
            raise KeyError(f"Key '{key}' not found")
        del self._store[key]
    def create(self, key: str, **overrides) -> Copyable:
        if key not in self._store:
            raise KeyError(f"Key '{key}' not found")
        return self._store[key].clone(**overrides)

if __name__ == "__main__":
    store = TemplateStore()
    store.register("small_blue_circle", Circle(radius=5.0, color="blue"))
    store.register("panel", Rectangle(width=100.0, height=50.0, color="gray"))

    c1 = store.create("small_blue_circle")
    c2 = store.create("small_blue_circle", color="red", radius=7.5)
    r1 = store.create("panel", width=120.0)

    print(c1, "area=", c1.area())
    print(c2, "area=", c2.area())
    print(r1, "area=", r1.area())

    c2.radius = 10.0
    print("After modification:")
    print("original template:", store.create("small_blue_circle"))
    print("modified clone:", c2)

    try:
        store.create("nonexistent")
    except KeyError as e:
        print("Error:", e)
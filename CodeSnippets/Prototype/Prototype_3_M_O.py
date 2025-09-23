import copy
import uuid
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self, deep: bool = True):
        pass

class Widget(Cloneable):
    def __init__(self, name: str, settings: dict = None, resources: list = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.settings = settings or {}
        self.resources = resources or []

    def clone(self, deep: bool = True):
        if deep:
            data = copy.deepcopy(self)
        else:
            data = copy.copy(self)
        data.id = str(uuid.uuid4())
        return data

    def update_settings(self, **overrides):
        self.settings.update(overrides)

    def add_resource(self, resource):
        if not resource:
            raise ValueError("Resource must be non-empty")
        self.resources.append(resource)

    def describe(self):
        return {
            "id": self.id,
            "name": self.name,
            "settings": dict(self.settings),
            "resources": list(self.resources),
        }

class TemplateStore:
    def __init__(self):
        self._store = {}

    def register(self, key: str, item: Cloneable):
        if not isinstance(item, Cloneable):
            raise TypeError("Item must implement cloneable interface")
        self._store[key] = item

    def unregister(self, key: str):
        self._store.pop(key, None)

    def create(self, key: str, deep: bool = True, overrides: dict = None):
        prototype = self._store.get(key)
        if prototype is None:
            raise KeyError(f"Template '{key}' not found")
        instance = prototype.clone(deep=deep)
        if overrides:
            if hasattr(instance, "update_settings"):
                instance.update_settings(**overrides)
            else:
                for k, v in overrides.items():
                    setattr(instance, k, v)
        return instance

if __name__ == "__main__":
    store = TemplateStore()
    base_widget = Widget("BaseButton", settings={"color": "blue", "size": "md"}, resources=["icon.svg"])
    store.register("button.base", base_widget)

    w1 = store.create("button.base", deep=True, overrides={"color": "red"})
    w2 = store.create("button.base", deep=False)
    w2.add_resource("temp.png")

    print("Original:", base_widget.describe())
    print("Deep clone with override:", w1.describe())
    print("Shallow clone modified:", w2.describe())
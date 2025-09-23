import copy
from abc import ABC, abstractmethod

class Clonable(ABC):
    @abstractmethod
    def clone(self, deep: bool = True):
        pass

class Document(Clonable):
    def __init__(self, title: str, content: str, metadata: dict):
        self.title = title
        self.content = content
        self.metadata = metadata

    def clone(self, deep: bool = True):
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def __repr__(self):
        return f"<Document title={self.title!r} metadata={self.metadata!r}>"

class TemplateRegistry:
    def __init__(self):
        self._store = {}

    def register(self, key: str, item: Clonable):
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string")
        if not isinstance(item, Clonable):
            raise TypeError("Item must support cloning")
        self._store[key] = item

    def unregister(self, key: str):
        self._store.pop(key, None)

    def create(self, key: str, deep: bool = True, **overrides):
        if key not in self._store:
            raise KeyError(f"Template '{key}' not found")
        clone = self._store[key].clone(deep=deep)
        for attr, val in overrides.items():
            if not hasattr(clone, attr):
                raise AttributeError(f"Attribute '{attr}' not found on cloned object")
            setattr(clone, attr, val)
        return clone

if __name__ == "__main__":
    registry = TemplateRegistry()
    base = Document("Monthly Report", "Contents...", {"authors": ["Alice"], "version": 1})
    registry.register("monthly", base)

    shallow_copy = registry.create("monthly", deep=False)
    deep_copy = registry.create("monthly", deep=True, title="Monthly Report - Copy")

    shallow_copy.metadata["authors"].append("Bob")
    deep_copy.metadata["authors"].append("Carol")

    print("Original:", base)
    print("Shallow copy:", shallow_copy)
    print("Deep copy:", deep_copy)
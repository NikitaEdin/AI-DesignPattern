import copy
from typing import Any, Dict


class ItemBase:
    def duplicate(self):
        return copy.deepcopy(self)


class Document(ItemBase):
    def __init__(self, title: str, content: str, metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.metadata = dict(metadata or {})

    def update_content(self, new_content: str):
        if not isinstance(new_content, str):
            raise ValueError("Content must be a string")
        self.content = new_content

    def __repr__(self):
        return f"Document(title={self.title!r}, content={self.content!r}, metadata={self.metadata!r})"


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, ItemBase] = {}

    def register(self, key: str, item: ItemBase):
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string")
        if key in self._store:
            raise KeyError(f"Key '{key}' is already registered")
        self._store[key] = item

    def unregister(self, key: str):
        try:
            del self._store[key]
        except KeyError:
            raise KeyError(f"No entry found for key '{key}'")

    def create(self, key: str, **overrides) -> ItemBase:
        try:
            prototype = self._store[key]
        except KeyError:
            raise KeyError(f"No template registered under key '{key}'")
        new_obj = prototype.duplicate()
        for attr, value in overrides.items():
            if not hasattr(new_obj, attr):
                raise AttributeError(f"Attribute '{attr}' not found on cloned object")
            setattr(new_obj, attr, value)
        return new_obj


if __name__ == "__main__":
    registry = TemplateRegistry()
    base_doc = Document(title="Report", content="Initial draft", metadata={"author": "Alice"})
    registry.register("report_v1", base_doc)

    copy1 = registry.create("report_v1")
    copy2 = registry.create("report_v1", title="Report - Final", metadata={"author": "Bob", "version": 2})

    copy1.update_content("Revised draft by reviewer")
    print("Base:", base_doc)
    print("Copy1:", copy1)
    print("Copy2:", copy2)

    try:
        registry.create("nonexistent")
    except KeyError as e:
        print("Error:", e)
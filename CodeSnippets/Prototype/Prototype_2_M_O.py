from abc import ABC, abstractmethod
import copy
import sys

class CloneableBase(ABC):
    @abstractmethod
    def clone(self):
        pass

class Document(CloneableBase):
    def __init__(self, title, content, metadata):
        self.title = title
        self.content = content
        self.metadata = metadata

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"Document(title={self.title!r}, content={self.content!r}, metadata={self.metadata!r})"

class TemplateRegistry:
    def __init__(self):
        self._store = {}

    def register(self, key, template):
        if not isinstance(template, CloneableBase):
            raise TypeError("Registered object must implement CloneableBase")
        self._store[key] = template

    def create(self, key, **overrides):
        if key not in self._store:
            raise KeyError(f"Template '{key}' not found")
        clone = self._store[key].clone()
        for attr, value in overrides.items():
            if not hasattr(clone, attr):
                raise AttributeError(f"Attribute '{attr}' not present on clone")
            setattr(clone, attr, value)
        return clone

def main():
    registry = TemplateRegistry()
    base_doc = Document("Report", "Initial content", {"author": "Alice", "version": 1})
    registry.register("report_base", base_doc)

    try:
        draft = registry.create("report_base", title="Draft Report")
        final = registry.create("report_base", title="Final Report", metadata={"author": "Bob", "version": 2})
    except (KeyError, TypeError, AttributeError) as e:
        print("Error:", e, file=sys.stderr)
        return

    draft.content += "\nAdded draft notes."
    draft.metadata["reviewed"] = False

    print("Base:", base_doc)
    print("Draft:", draft)
    print("Final:", final)

if __name__ == "__main__":
    main()
import copy
from dataclasses import dataclass, field, fields
from typing import Any, Dict

class ClonableBase:
    def clone(self, **overrides) -> "ClonableBase":
        if not hasattr(self, "__dict__") and not hasattr(self, "__slots__"):
            raise TypeError("Object is not clonable")
        obj = copy.deepcopy(self)
        valid_attrs = {f.name for f in fields(self)} if hasattr(self, "__dataclass_fields__") else set(obj.__dict__.keys())
        for key, value in overrides.items():
            if key not in valid_attrs:
                raise ValueError(f"Invalid attribute for cloning: {key}")
            setattr(obj, key, value)
        return obj

@dataclass
class Document(ClonableBase):
    title: str
    content: str
    tags: list = field(default_factory=list)

@dataclass
class ImageAsset(ClonableBase):
    name: str
    pixels: list = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, ClonableBase] = {}
        self._counts: Dict[str, int] = {}

    def register(self, key: str, template: ClonableBase):
        if not isinstance(template, ClonableBase):
            raise TypeError("Only clonable objects can be registered")
        self._store[key] = template
        self._counts[key] = 0

    def create(self, key: str, **overrides) -> ClonableBase:
        template = self._store.get(key)
        if template is None:
            raise KeyError(f"No template registered under key: {key}")
        instance = template.clone(**overrides)
        self._counts[key] += 1
        return instance

    def usage_count(self, key: str) -> int:
        return self._counts.get(key, 0)

if __name__ == "__main__":
    registry = TemplateRegistry()

    doc_template = Document(title="Report", content="Initial", tags=["draft"])
    img_template = ImageAsset(name="Logo", pixels=[[0]*3]*3, metadata={"format": "png"})

    registry.register("report", doc_template)
    registry.register("logo", img_template)

    doc1 = registry.create("report", title="Q1 Report")
    doc2 = registry.create("report", tags=["final", "approved"])
    img1 = registry.create("logo", metadata={"format": "svg"})

    doc1.tags.append("review")
    doc2.content = "Finalized content"

    print(doc_template)
    print(doc1)
    print(doc2)
    print(img_template)
    print(img1)
    print("Report clones created:", registry.usage_count("report"))
    try:
        registry.create("report", non_existing_attr=123)
    except Exception as e:
        print("Error during cloning:", e)
import copy
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict


class BaseCloneable:
    def clone(self, deep: bool = True, preserve_id: bool = False, overrides: Dict[str, Any] = None):
        obj = copy.deepcopy(self) if deep else copy.copy(self)
        if not preserve_id and hasattr(obj, "uid"):
            obj.uid = uuid.uuid4().hex
        if hasattr(obj, "version"):
            try:
                obj.version = int(getattr(self, "version", 0)) + 1
            except Exception:
                obj.version = getattr(self, "version", 0)
        if overrides:
            for k, v in overrides.items():
                setattr(obj, k, v)
        return obj


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, BaseCloneable] = {}

    def register(self, key: str, template: BaseCloneable):
        if not isinstance(template, BaseCloneable):
            raise TypeError("Only BaseCloneable instances can be registered")
        self._store[key] = template

    def create(self, key: str, deep: bool = True, preserve_id: bool = False, overrides: Dict[str, Any] = None):
        if key not in self._store:
            raise KeyError(f"No template registered under key: {key}")
        return self._store[key].clone(deep=deep, preserve_id=preserve_id, overrides=overrides)


@dataclass
class ResourceHandle(BaseCloneable):
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)
    connection_uri: str = ""
    runtime_state: dict = field(default_factory=dict)
    version: int = 0

    def __deepcopy__(self, memo):
        new = type(self)(
            uid=uuid.uuid4().hex,
            connection_uri=self.connection_uri,
            runtime_state=copy.deepcopy(self.runtime_state, memo),
            version=int(self.version) + 1,
        )
        return new


@dataclass
class Document(BaseCloneable):
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)
    title: str = ""
    paragraphs: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    resource: ResourceHandle = None
    version: int = 0

    def summarize(self):
        return {
            "uid": self.uid,
            "title": self.title,
            "paragraphs": list(self.paragraphs),
            "metadata": dict(self.metadata),
            "resource_uid": getattr(self.resource, "uid", None),
            "version": self.version,
        }


if __name__ == "__main__":
    registry = TemplateRegistry()

    base_resource = ResourceHandle(connection_uri="redis://localhost:6379", runtime_state={"connections": 1})
    template_doc = Document(
        title="Template Doc",
        paragraphs=["Intro", "Body", "Conclusion"],
        metadata={"author": "Alice", "tags": ["template", "example"]},
        resource=base_resource,
        version=1,
    )

    registry.register("standard", template_doc)

    clone1 = registry.create("standard", deep=True)
    clone2 = registry.create("standard", deep=False, overrides={"title": "Shallow Copy Title"})
    clone3 = registry.create("standard", deep=True, overrides={"metadata": {"author": "Bob"}})

    clone1.paragraphs.append("Appendix")
    clone1.resource.runtime_state["connections"] = 5

    clone2.paragraphs.append("Footnote")
    clone2.resource.runtime_state["connections"] = 9

    print("Original:", template_doc.summarize())
    print("Deep Clone (modified):", clone1.summarize())
    print("Shallow Clone (modified):", clone2.summarize())
    print("Deep Clone with override:", clone3.summarize())
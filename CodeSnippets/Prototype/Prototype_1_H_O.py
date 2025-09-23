import copy
import uuid
import threading
from typing import Any, Dict


class Cloneable:
    _exclude_from_clone = frozenset()
    _reset_on_clone = ()

    def clone(self, deep: bool = True, overrides: Dict[str, Any] = None):
        overrides = overrides or {}
        state = {}
        for k, v in self.__dict__.items():
            if k in self._exclude_from_clone:
                state[k] = v
            else:
                try:
                    state[k] = copy.deepcopy(v) if deep else copy.copy(v)
                except Exception:
                    state[k] = v
        obj = self.__class__.__new__(self.__class__)
        obj.__dict__.update(state)
        if hasattr(obj, "id") and "id" not in overrides:
            obj.id = str(uuid.uuid4())
        for name in getattr(obj, "_reset_on_clone", ()):
            try:
                setattr(obj, name, type(getattr(self, name))())
            except Exception:
                setattr(obj, name, None)
        for k, v in overrides.items():
            setattr(obj, k, v)
        hook = getattr(obj, "_after_clone", None)
        if callable(hook):
            hook()
        return obj


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, Cloneable] = {}

    def register(self, key: str, template: Cloneable, replace: bool = False):
        if not replace and key in self._store:
            raise KeyError(f"Key exists: {key}")
        self._store[key] = template

    def unregister(self, key: str):
        self._store.pop(key, None)

    def create(self, key: str, deep: bool = True, **overrides):
        template = self._store.get(key)
        if template is None:
            raise KeyError(f"No template: {key}")
        return template.clone(deep=deep, overrides=overrides)


class Document(Cloneable):
    _exclude_from_clone = frozenset({"file_handle"})
    _reset_on_clone = ("lock",)

    def __init__(self, title: str, paragraphs: list = None, metadata: dict = None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.paragraphs = list(paragraphs or [])
        self.metadata = dict(metadata or {})
        self.lock = threading.Lock()
        self.file_handle = None

    def add_paragraph(self, text: str):
        self.paragraphs.append(text)

    def _after_clone(self):
        self.metadata = dict(self.metadata)


class Widget(Cloneable):
    def __init__(self, name: str, config: dict = None, components: list = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.config = dict(config or {})
        self.components = list(components or [])

    def add_component(self, comp: Any):
        self.components.append(comp)


if __name__ == "__main__":
    registry = TemplateRegistry()

    doc_template = Document(
        "Master Doc",
        paragraphs=["Intro", "Body", "Conclusion"],
        metadata={"author": "Alice", "version": 1},
    )
    widget_template = Widget("Panel", config={"theme": "dark"}, components=[doc_template])

    registry.register("doc:master", doc_template)
    registry.register("widget:panel", widget_template)

    d1 = registry.create("doc:master", deep=True)
    d2 = registry.create("doc:master", deep=False)
    d1.add_paragraph("Appended to deep clone")
    d2.add_paragraph("Appended to shallow clone")

    w1 = registry.create("widget:panel", deep=True)
    w2 = registry.create("widget:panel", deep=False)

    w1.components[0].metadata["version"] = 2
    w2.components[0].metadata["version"] = 3

    print("Template doc paragraphs:", doc_template.paragraphs)
    print("Deep clone doc paragraphs:", d1.paragraphs)
    print("Shallow clone doc paragraphs:", d2.paragraphs)
    print("Template widget component doc version:", widget_template.components[0].metadata["version"])
    print("Deep widget's component doc version:", w1.components[0].metadata["version"])
    print("Shallow widget's component doc version:", w2.components[0].metadata["version"])
    print("Original doc id:", doc_template.id)
    print("Deep clone id:", d1.id)
    print("Shallow clone id:", d2.id)
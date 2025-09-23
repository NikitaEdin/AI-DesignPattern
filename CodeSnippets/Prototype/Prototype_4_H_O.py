import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

class Duplicable(ABC):
    @abstractmethod
    def duplicate(self, deep: bool = True, postprocess: Optional[Callable[['Duplicable'], None]] = None) -> 'Duplicable':
        pass

@dataclass
class Document(Duplicable):
    title: str
    content: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    reference: Optional['Document'] = None

    def duplicate(self, deep: bool = True, postprocess: Optional[Callable[['Document'], None]] = None) -> 'Document':
        try:
            result = copy.deepcopy(self) if deep else copy.copy(self)
        except Exception:
            result = copy.copy(self)
            if deep:
                for k, v in self.__dict__.items():
                    try:
                        setattr(result, k, copy.deepcopy(v))
                    except Exception:
                        setattr(result, k, copy.copy(v))
        if postprocess:
            postprocess(result)
        return result

@dataclass
class Configuration(Duplicable):
    values: Dict[str, Any] = field(default_factory=dict)
    tags: list = field(default_factory=list)
    locked: bool = False

    def duplicate(self, deep: bool = True, postprocess: Optional[Callable[['Configuration'], None]] = None) -> 'Configuration':
        try:
            result = copy.deepcopy(self) if deep else copy.copy(self)
        except Exception:
            result = copy.copy(self)
            if deep:
                for k, v in self.__dict__.items():
                    try:
                        setattr(result, k, copy.deepcopy(v))
                    except Exception:
                        setattr(result, k, copy.copy(v))
        if postprocess:
            postprocess(result)
        return result

class BlueprintRegistry:
    def __init__(self):
        self._store: Dict[str, Duplicable] = {}

    def register(self, name: str, template: Duplicable):
        if not isinstance(template, Duplicable):
            raise TypeError("template must implement Duplicable")
        self._store[name] = template

    def unregister(self, name: str):
        self._store.pop(name, None)

    def create(self, name: str, deep: bool = True, postprocess: Optional[Callable[[Duplicable], None]] = None) -> Duplicable:
        template = self._store.get(name)
        if template is None:
            raise KeyError(f"no template registered under '{name}'")
        return template.duplicate(deep=deep, postprocess=postprocess)

if __name__ == "__main__":
    registry = BlueprintRegistry()

    doc = Document(title="Report", content=["intro", "body"], metadata={"author": "Alice"})
    doc.reference = doc
    cfg = Configuration(values={"threshold": 10}, tags=["v1"], locked=False)

    registry.register("report", doc)
    registry.register("config", cfg)

    deep_doc = registry.create("report", deep=True)
    shallow_doc = registry.create("report", deep=False)
    deep_cfg = registry.create("config", deep=True, postprocess=lambda c: c.tags.append("deep-copied"))

    doc.content.append("conclusion")
    doc.metadata["edited"] = True
    cfg.values["threshold"] = 20

    print("original content:", doc.content)
    print("deep copy content:", deep_doc.content)
    print("shallow copy content (shared list):", shallow_doc.content)
    print("original metadata:", doc.metadata)
    print("deep copy metadata:", deep_doc.metadata)
    print("original config threshold:", cfg.values["threshold"])
    print("deep copy config threshold:", deep_cfg.values["threshold"])
    print("deep config tags:", deep_cfg.tags)
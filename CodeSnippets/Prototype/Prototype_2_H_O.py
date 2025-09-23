import copy
import threading
import dataclasses
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Any, Dict, List

class Cloneable:
    def clone(self, deep: bool = True, overrides: Dict[str, Any] = None):
        return self._base_clone(deep=deep, overrides=overrides or {})

    def _base_clone(self, deep: bool, overrides: Dict[str, Any]):
        try:
            new_obj = copy.deepcopy(self) if deep else copy.copy(self)
        except Exception:
            new_obj = self._fallback_clone(deep)
        for k, v in overrides.items():
            if not hasattr(new_obj, k):
                raise AttributeError(f"Unknown attribute '{k}' for override")
            setattr(new_obj, k, copy.deepcopy(v) if deep else v)
        if new_obj is not self:
            new_obj._post_clone(deep=deep, original=self)
        return new_obj

    def _post_clone(self, deep: bool, original: "Cloneable"):
        return

    def _fallback_clone(self, deep: bool):
        raise RuntimeError("Clone failed and no fallback is provided")

class Registry:
    def __init__(self):
        self._lock = threading.RLock()
        self._store: Dict[str, Cloneable] = {}

    def register(self, name: str, prototype: Cloneable):
        with self._lock:
            if name in self._store:
                raise KeyError(f"Name '{name}' already registered")
            self._store[name] = prototype

    def create(self, name: str, deep: bool = True, overrides: Dict[str, Any] = None):
        with self._lock:
            if name not in self._store:
                raise KeyError(f"Unknown prototype '{name}'")
            proto = self._store[name]
        return proto.clone(deep=deep, overrides=overrides or {})

@dataclass
class Leaf(Cloneable):
    uid: str = field(default_factory=lambda: str(uuid4()))
    version: int = 1
    payload: Dict[str, Any] = field(default_factory=dict)

    def _post_clone(self, deep: bool, original: "Leaf"):
        if id(self) != id(original):
            self.uid = str(uuid4())
            self.version = original.version + 1

@dataclass
class Group(Cloneable):
    name: str
    parts: List[Cloneable] = field(default_factory=list)

    def _post_clone(self, deep: bool, original: "Group"):
        for i, part in enumerate(self.parts):
            if i < len(original.parts):
                orig_part = original.parts[i]
                if id(part) != id(orig_part) and isinstance(part, Cloneable):
                    part._post_clone(deep=deep, original=orig_part)

if __name__ == "__main__":
    registry = Registry()

    leaf_proto = Leaf(payload={"value": 42})
    group_proto = Group(name="bundle", parts=[leaf_proto])

    registry.register("leaf", leaf_proto)
    registry.register("group", group_proto)

    shallow_group = registry.create("group", deep=False)
    deep_group = registry.create("group", deep=True)

    print("Prototype leaf uid:", leaf_proto.uid, "version:", leaf_proto.version)
    print("Shallow group's leaf uid:", shallow_group.parts[0].uid, "version:", shallow_group.parts[0].version)
    print("Deep group's leaf uid:", deep_group.parts[0].uid, "version:", deep_group.parts[0].version)
    print("Shared leaf in shallow:", id(shallow_group.parts[0]) == id(leaf_proto))
    print("Shared leaf in deep:", id(deep_group.parts[0]) == id(leaf_proto))
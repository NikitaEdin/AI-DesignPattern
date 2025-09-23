from abc import ABC, abstractmethod
from threading import RLock
from typing import Callable, Dict, Any


class BaseItem(ABC):
    @abstractmethod
    def operate(self) -> str:
        pass


class AlphaItem(BaseItem):
    def __init__(self, name: str = "alpha", multiplier: int = 1):
        self.name = name
        self.multiplier = int(multiplier)

    def operate(self) -> str:
        return f"{self.name} operated x{self.multiplier}"


class BetaItem(BaseItem):
    def __init__(self, level: int = 0):
        self.level = int(level)

    def operate(self) -> str:
        return f"beta level {self.level}"


class ProductMaker:
    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()

    def register(self, key: str, creator: Callable[..., BaseItem], *, singleton: bool = False, replace: bool = False):
        if not callable(creator):
            raise TypeError("creator must be callable")
        with self._lock:
            if key in self._registry and not replace:
                raise KeyError(f"key '{key}' already registered")
            self._registry[key] = {"creator": creator, "singleton": bool(singleton), "instance": None}

    def unregister(self, key: str):
        with self._lock:
            if key not in self._registry:
                raise KeyError(f"key '{key}' not found")
            del self._registry[key]

    def create(self, key: str, **kwargs) -> BaseItem:
        with self._lock:
            entry = self._registry.get(key)
            if entry is None:
                raise KeyError(f"unknown key '{key}'")
            if entry["singleton"] and entry["instance"] is not None:
                return entry["instance"]
            creator = entry["creator"]
        try:
            obj = creator(**kwargs)
        except Exception as exc:
            raise RuntimeError(f"creator for '{key}' failed: {exc}") from exc
        if not isinstance(obj, BaseItem):
            raise TypeError("creator must return an instance of BaseItem")
        if entry["singleton"]:
            with self._lock:
                if entry["instance"] is None:
                    entry["instance"] = obj
                else:
                    obj = entry["instance"]
        return obj

    def available(self):
        with self._lock:
            return list(self._registry.keys())


if __name__ == "__main__":
    maker = ProductMaker()

    maker.register("alpha", lambda name="alpha", multiplier=1: AlphaItem(name=name, multiplier=multiplier))
    maker.register("beta", lambda level=0: BetaItem(level=level))
    maker.register("alpha_single", lambda name="singleton", multiplier=2: AlphaItem(name=name, multiplier=multiplier), singleton=True)

    a1 = maker.create("alpha", name="A-one", multiplier=3)
    a2 = maker.create("alpha", name="A-two", multiplier=5)
    b1 = maker.create("beta", level=7)

    s1 = maker.create("alpha_single", name="S", multiplier=4)
    s2 = maker.create("alpha_single", name="Ignored", multiplier=9)

    print(a1.operate())
    print(a2.operate())
    print(b1.operate())
    print(s1.operate(), "same_instance:", s1 is s2)

    print("available keys:", maker.available())

    try:
        maker.create("unknown")
    except KeyError as e:
        print("expected error:", e)
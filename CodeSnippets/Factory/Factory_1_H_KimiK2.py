import threading
from functools import wraps
from abc import ABC, abstractmethod

_registry = {}
_registry_lock = threading.RLock()

def register(kind):
    def decorator(cls):
        with _registry_lock:
            _registry[kind] = cls
        return cls
    return decorator

class Product(ABC):
    @abstractmethod
    def operate(self): ...

class Creator(ABC):
    @abstractmethod
    def _prepare(self, **opts): ...

    def craft(self, kind, **opts):
        with _registry_lock:
            cls = _registry.get(kind)
        if not cls:
            raise ValueError(f"Unknown kind: {kind}")
        params = self._prepare(**opts)
        return cls(**params)

class CachedCreator(Creator):
    def __init__(self):
        self._cache = {}
        self._cache_lock = threading.RLock()

    def _prepare(self, **opts):
        return opts

    def craft(self, kind, **opts):
        key = (kind, tuple(sorted(opts.items())))
        with self._cache_lock:
            if key in self._cache:
                return self._cache[key]
        instance = super().craft(kind, **opts)
        with self._cache_lock:
            self._cache[key] = instance
        return instance

@register("A")
class ConcreteProductA(Product):
    def __init__(self, value=0):
        self.value = value
    def operate(self):
        return f"A:{self.value}"

@register("B")
class ConcreteProductB(Product):
    def __init__(self, value=0):
        self.value = value
    def operate(self):
        return f"B:{self.value * 2}"

if __name__ == "__main__":
    maker = CachedCreator()
    p1 = maker.craft("A", value=10)
    p2 = maker.craft("A", value=10)
    p3 = maker.craft("B", value=5)
    assert p1 is p2
    print(p1.operate(), p3.operate())
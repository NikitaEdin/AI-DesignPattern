import threading
import inspect
from typing import Callable, Dict, Iterable, List, Optional, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T", bound="ProductBase")


class ProductBase(ABC):
    @abstractmethod
    def perform(self) -> str:
        pass


class Widget(ProductBase):
    def __init__(self, name: str = "widget"):
        self.name = name

    def perform(self) -> str:
        return f"Widget:{self.name}"


class Gizmo(ProductBase):
    def __init__(self, label: str = "gizmo"):
        self.label = label

    def perform(self) -> str:
        return f"Gizmo:{self.label}"


class UnknownProductError(KeyError):
    pass


class CreatorRegistry:
    def __init__(self):
        self._lock = threading.RLock()
        self._creators: Dict[str, Callable[..., ProductBase]] = {}

    def _normalize_creator(self, creator: Callable[..., object]) -> Callable[..., ProductBase]:
        # Return a callable that always yields a ProductBase or raises TypeError
        def wrapper(*args, **kwargs) -> ProductBase:
            result = creator(*args, **kwargs)
            if isinstance(result, ProductBase):
                return result
            if callable(result):
                # attempt a second call without arguments (common pattern)
                second = result()
                if isinstance(second, ProductBase):
                    return second
            raise TypeError("Creator did not produce a ProductBase instance")
        return wrapper

    def register(self, key: str, creator: Optional[Callable[..., object]] = None):
        if creator is None:
            def decorator(fn: Callable[..., object]):
                with self._lock:
                    self._creators[key] = self._normalize_creator(fn)
                return fn
            return decorator
        with self._lock:
            self._creators[key] = self._normalize_creator(creator)
        return creator

    def create(self, key: str, *args, **kwargs) -> ProductBase:
        with self._lock:
            try:
                creator = self._creators[key]
            except KeyError:
                raise UnknownProductError(f"Unknown product key: {key}") from None
        product = creator(*args, **kwargs)
        if not isinstance(product, ProductBase):
            raise TypeError("Creator did not return a ProductBase")
        return product

    def unregister(self, key: str) -> None:
        with self._lock:
            self._creators.pop(key, None)

    def keys(self) -> List[str]:
        with self._lock:
            return list(self._creators.keys())

    def lazy_creator(self, cls: Callable[..., T]) -> Callable[..., T]:
        def creator(*args, **kwargs) -> T:
            return cls(*args, **kwargs)
        return creator


_registry = CreatorRegistry()


# Usage examples
@_registry.register("widget")
def make_widget(name: str = "alpha") -> ProductBase:
    return Widget(name)


class _GizmoMaker:
    def __init__(self, label: str = "beta"):
        self.label = label

    def __call__(self) -> ProductBase:
        return Gizmo(self.label)


# Registering a class-style creator (its instances are callable).
# Normalization wraps it so calling the registered creator returns a ProductBase.
_registry.register("gizmo", _GizmoMaker)


# Registering a simple constructor via helper
_registry.register("simple_widget", _registry.lazy_creator(Widget))


if __name__ == "__main__":
    w = _registry.create("widget", "omega")
    g = _registry.create("gizmo", "gamma")
    s = _registry.create("simple_widget", "delta")
    print(w.perform())
    print(g.perform())
    print(s.perform())
    print("available keys:", _registry.keys())
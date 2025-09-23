import threading
from abc import ABC, abstractmethod
from typing import Callable, Dict, Any, Tuple, Optional


class ProductCreationError(Exception):
    pass


class ProductMissingError(Exception):
    pass


class BaseProduct(ABC):
    @abstractmethod
    def operate(self) -> str:
        pass


class JsonHandler(BaseProduct):
    def __init__(self, indent: int = 2):
        if indent < 0:
            raise ProductCreationError("indent must be non-negative")
        self.indent = indent

    def operate(self) -> str:
        return f"JSON handler with indent={self.indent}"


class XmlHandler(BaseProduct):
    def __init__(self, version: str = "1.0"):
        if not version:
            raise ProductCreationError("version is required")
        self.version = version

    def operate(self) -> str:
        return f"XML handler version={self.version}"


class CsvHandler(BaseProduct):
    def __init__(self, delimiter: str = ","):
        if len(delimiter) != 1:
            raise ProductCreationError("delimiter must be a single character")
        self.delimiter = delimiter

    def operate(self) -> str:
        return f"CSV handler delimiter='{self.delimiter}'"


class ProducerRegistry:
    def __init__(self):
        self._registry: Dict[str, Tuple[Callable[..., BaseProduct], bool]] = {}
        self._singletons: Dict[str, BaseProduct] = {}
        self._lock = threading.RLock()

    def register(self, key: str, creator: Callable[..., BaseProduct], singleton: bool = False, override: bool = False) -> None:
        if not callable(creator):
            raise TypeError("creator must be callable")
        with self._lock:
            if key in self._registry and not override:
                raise ProductCreationError(f"key '{key}' already registered")
            self._registry[key] = (creator, bool(singleton))
            if not singleton and key in self._singletons:
                self._singletons.pop(key, None)

    def register_decorator(self, key: str, singleton: bool = False, override: bool = False):
        def decorator(cls):
            self.register(key, cls, singleton=singleton, override=override)
            return cls
        return decorator

    def make(self, key: str, *, force_new: bool = False, **kwargs) -> BaseProduct:
        with self._lock:
            entry = self._registry.get(key)
            if entry is None:
                raise ProductMissingError(f"no product registered under key '{key}'")
            creator, is_singleton = entry
            if is_singleton and not force_new:
                if key in self._singletons:
                    return self._singletons[key]
                instance = self._safe_create(creator, **kwargs)
                self._singletons[key] = instance
                return instance
            return self._safe_create(creator, **kwargs)

    def _safe_create(self, creator: Callable[..., BaseProduct], **kwargs) -> BaseProduct:
        try:
            instance = creator(**kwargs)
        except TypeError as e:
            raise ProductCreationError(f"invalid arguments for creator: {e}") from e
        if not isinstance(instance, BaseProduct):
            raise ProductCreationError("creator did not return a BaseProduct instance")
        return instance

    def available_keys(self):
        with self._lock:
            return list(self._registry.keys())


if __name__ == "__main__":
    registry = ProducerRegistry()
    registry.register("json", JsonHandler)
    registry.register("xml", XmlHandler, singleton=True)
    @registry.register_decorator("csv")
    class CSV(CsvHandler):
        pass

    p1 = registry.make("json", indent=4)
    p2 = registry.make("xml", version="1.1")
    p3 = registry.make("xml")  # singleton returns same instance as p2
    p4 = registry.make("csv", delimiter=";")

    print(p1.operate())
    print(p2.operate())
    print("xml same instance:", p2 is p3)
    print(p4.operate())

    try:
        registry.make("unknown")
    except Exception as e:
        print("error:", type(e).__name__, str(e))
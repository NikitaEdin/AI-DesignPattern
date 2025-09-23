from abc import ABC, abstractmethod
from threading import RLock
from time import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import copy
import sys

class Component(ABC):
    @abstractmethod
    def execute(self, data: Any) -> Any:
        raise NotImplementedError

class CoreService(Component):
    def __init__(self, name: str = "CoreService"):
        self.name = name

    def execute(self, data: Any) -> Any:
        if isinstance(data, dict):
            result = dict(data)
            result["_processed_by"] = self.name
            return result
        return {"value": data, "_processed_by": self.name}

class WrapperBase(Component):
    def __init__(self, inner: Component):
        if not isinstance(inner, Component):
            raise TypeError("inner must implement Component")
        self._inner: Component = inner
        self._enabled = True
        self._lock = RLock()

    def execute(self, data: Any) -> Any:
        with self._lock:
            if not self._enabled:
                return self._inner.execute(data)
            return self._handle(data)

    def _handle(self, data: Any) -> Any:
        return self._inner.execute(data)

    def set_inner(self, inner: Component) -> None:
        if not isinstance(inner, Component):
            raise TypeError("inner must implement Component")
        with self._lock:
            self._inner = inner

    def enable(self) -> None:
        with self._lock:
            self._enabled = True

    def disable(self) -> None:
        with self._lock:
            self._enabled = False

    def is_enabled(self) -> bool:
        with self._lock:
            return bool(self._enabled)

    def get_chain(self) -> List[Tuple[str, bool]]:
        chain: List[Tuple[str, bool]] = []
        node: Optional[Component] = self
        while isinstance(node, WrapperBase):
            chain.append((node.__class__.__name__, node.is_enabled()))
            node = node._inner
        chain.append((node.__class__.__name__, True))
        return chain

    def find_layer(self, cls: type) -> Optional['WrapperBase']:
        node: Optional[Component] = self
        while isinstance(node, WrapperBase):
            if isinstance(node, cls):
                return node
            node = node._inner
        return None

    def temp_disable(self):
        parent = self
        class _Ctx:
            def __enter__(self_non):
                self._lock.acquire()
                self_non._was_enabled = parent._enabled
                parent._enabled = False
                self._lock.release()
                return parent
            def __exit__(self_non, exc_type, exc, tb):
                self._lock.acquire()
                parent._enabled = getattr(self_non, "_was_enabled", True)
                self._lock.release()
        return _Ctx()

class LoggingLayer(WrapperBase):
    def __init__(self, inner: Component, writer: Callable[[str], None] = None):
        super().__init__(inner)
        self._writer = writer or (lambda s: sys.stdout.write(s + "\n"))

    def _handle(self, data: Any) -> Any:
        ts = time()
        self._writer(f"[{ts:.6f}] -> {self.__class__.__name__} incoming: {repr(data)}")
        result = self._inner.execute(data)
        ts2 = time()
        self._writer(f"[{ts2:.6f}] <- {self.__class__.__name__} result: {repr(result)} (t={ts2-ts:.6f}s)")
        return result

class CacheLayer(WrapperBase):
    def __init__(self, inner: Component, max_entries: int = 256):
        super().__init__(inner)
        self._cache: Dict[int, Any] = {}
        self._max = max_entries

    def _make_key(self, data: Any) -> int:
        try:
            return hash(self._freeze(data))
        except Exception:
            return hash(repr(data))

    def _freeze(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return tuple(sorted((k, self._freeze(v)) for k, v in obj.items()))
        if isinstance(obj, (list, tuple, set)):
            return tuple(self._freeze(x) for x in obj)
        return obj

    def _handle(self, data: Any) -> Any:
        key = self._make_key(data)
        with self._lock:
            if key in self._cache:
                return copy.deepcopy(self._cache[key])
        result = self._inner.execute(data)
        with self._lock:
            if len(self._cache) >= self._max:
                self._cache.clear()
            self._cache[key] = copy.deepcopy(result)
        return result

class ValidationLayer(WrapperBase):
    def __init__(self, inner: Component, validator: Callable[[Any], bool]):
        super().__init__(inner)
        self._validator = validator

    def _handle(self, data: Any) -> Any:
        if not self._validator(data):
            raise ValueError(f"validation failed for data: {repr(data)}")
        return self._inner.execute(data)

if __name__ == "__main__":
    core = CoreService("PrimaryProcessor")
    cached = CacheLayer(core, max_entries=128)
    logged = LoggingLayer(cached)
    validated = ValidationLayer(logged, validator=lambda d: isinstance(d, dict) and "id" in d)

    chain = validated.get_chain()
    print("Initial chain:", chain)

    payload = {"id": 1, "value": 100}
    print("First call result:", validated.execute(payload))
    print("Second call (should be cached):", validated.execute(payload))

    try:
        print("Invalid input test:")
        validated.execute("not a dict")
    except Exception as e:
        print("Caught:", repr(e))

    cached_layer = validated.find_layer(CacheLayer)
    if cached_layer:
        cached_layer.disable()
    print("After disabling cache, call result (recomputed):", validated.execute(payload))

    with logged.temp_disable():
        print("Within temp-disable logging, call result:", validated.execute(payload))

    print("Final chain:", validated.get_chain())
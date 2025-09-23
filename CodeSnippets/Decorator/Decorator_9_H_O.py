import time
import threading
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Optional, Dict, Tuple


class ServiceInterface(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass


class BasicService(ServiceInterface):
    def __init__(self, name: str = "Basic"):
        self.name = name

    def execute(self, x: int, y: int = 1) -> int:
        total = 0
        for i in range(x):
            total += y
        return total


class WrapperBase(ServiceInterface):
    def __init__(self, component: ServiceInterface):
        object.__setattr__(self, "_component", component)
        object.__setattr__(self, "_enabled", True)
        object.__setattr__(self, "_lock", threading.RLock())

    def execute(self, *args, **kwargs):
        return self._component.execute(*args, **kwargs)

    def unwrap(self) -> ServiceInterface:
        comp = self._component
        while isinstance(comp, WrapperBase):
            comp = comp._component
        return comp

    def enable(self):
        with self._lock:
            self._enabled = True

    def disable(self):
        with self._lock:
            self._enabled = False

    def __enter__(self):
        self._prev = self._enabled
        self.disable()
        return self

    def __exit__(self, exc_type, exc, tb):
        if getattr(self, "_prev", False):
            self.enable()
        return False

    def __getattr__(self, item):
        return getattr(self._component, item)

    def __setattr__(self, key, value):
        if key in {"_component", "_enabled", "_lock", "_prev"}:
            object.__setattr__(self, key, value)
        else:
            setattr(self._component, key, value)


class LoggingWrapper(WrapperBase):
    def __init__(self, component: ServiceInterface, logger: Optional[Callable[[str], None]] = None):
        super().__init__(component)
        object.__setattr__(self, "logger", logger or (lambda msg: print(msg)))

    def execute(self, *args, **kwargs):
        if not self._enabled:
            return super().execute(*args, **kwargs)
        start = time.time()
        try:
            self.logger(f"[LOG] Calling {self._component.__class__.__name__}.execute args={args} kwargs={kwargs}")
            result = self._component.execute(*args, **kwargs)
            duration = (time.time() - start)
            self.logger(f"[LOG] {self._component.__class__.__name__}.execute returned={result} duration={duration:.6f}s")
            return result
        except Exception as e:
            duration = (time.time() - start)
            self.logger(f"[LOG] {self._component.__class__.__name__}.execute raised={e!r} after {duration:.6f}s")
            raise


class TimingWrapper(WrapperBase):
    def __init__(self, component: ServiceInterface, warn_threshold: Optional[float] = None):
        super().__init__(component)
        object.__setattr__(self, "warn_threshold", warn_threshold)

    def execute(self, *args, **kwargs):
        if not self._enabled:
            return super().execute(*args, **kwargs)
        start = time.perf_counter()
        result = self._component.execute(*args, **kwargs)
        elapsed = time.perf_counter() - start
        if self.warn_threshold is not None and elapsed > self.warn_threshold:
            print(f"[TIME] Warning: {self._component.__class__.__name__} took {elapsed:.6f}s")
        else:
            print(f"[TIME] {self._component.__class__.__name__} took {elapsed:.6f}s")
        return result


class CachingWrapper(WrapperBase):
    def __init__(self, component: ServiceInterface, ttl: Optional[float] = None, max_entries: int = 1024):
        super().__init__(component)
        object.__setattr__(self, "_cache", {})  # type: Dict[Tuple, Tuple[float, Any]]
        object.__setattr__(self, "_ttl", ttl)
        object.__setattr__(self, "_max", max_entries)

    def _make_key(self, args, kwargs):
        try:
            return (args, tuple(sorted(kwargs.items())))
        except Exception:
            return (repr(args), repr(sorted(kwargs.items())))

    def execute(self, *args, **kwargs):
        if not self._enabled:
            return super().execute(*args, **kwargs)
        key = self._make_key(args, kwargs)
        now = time.time()
        cache = self._cache
        entry = cache.get(key)
        if entry:
            ts, value = entry
            if self._ttl is None or (now - ts) <= self._ttl:
                return value
            else:
                cache.pop(key, None)
        result = self._component.execute(*args, **kwargs)
        if len(cache) >= self._max:
            oldest = min(cache.items(), key=lambda kv: kv[1][0])[0]
            cache.pop(oldest, None)
        cache[key] = (now, result)
        return result


if __name__ == "__main__":
    svc = BasicService(name="Counter")
    svc = LoggingWrapper(svc)
    svc = TimingWrapper(svc, warn_threshold=0.0001)
    svc = CachingWrapper(svc, ttl=1.0, max_entries=100)

    print("First call (computed):", svc.execute(1000, y=2))
    print("Second call (cached):", svc.execute(1000, y=2))

    with svc:
        print("Temporarily disabled wrappers:", svc.execute(1000, y=2))

    original = svc.unwrap()
    print("Unwrapped original:", original.__class__.__name__, original.name)
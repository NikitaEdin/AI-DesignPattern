import time
import threading
import pickle
from collections import OrderedDict

class Component:
    def execute(self, data):
        raise NotImplementedError

class BasicService(Component):
    def execute(self, data):
        time.sleep(0.02)
        if isinstance(data, list):
            return [x * 2 for x in data]
        if isinstance(data, dict):
            return {k: v * 2 for k, v in data.items()}
        return data * 2

class BaseWrapper(Component):
    def __init__(self, component):
        if not isinstance(component, Component):
            raise TypeError("component must implement Component")
        self._component = component
    def execute(self, data):
        return self._component.execute(data)

class CacheWrapper(BaseWrapper):
    def __init__(self, component, max_entries=128):
        super().__init__(component)
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        self._max = max_entries
        self._cache = OrderedDict()
        self._lock = threading.Lock()

    def _make_key(self, data):
        try:
            hash(("k", data))
            return ("k", data)
        except TypeError:
            try:
                return ("k", pickle.dumps(data))
            except Exception:
                return ("k", repr(data))

    def execute(self, data):
        key = self._make_key(data)
        with self._lock:
            if key in self._cache:
                value = self._cache.pop(key)
                self._cache[key] = value
                return value
        result = super().execute(data)
        with self._lock:
            self._cache[key] = result
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)
        return result

if __name__ == "__main__":
    service = BasicService()
    cached_service = CacheWrapper(service, max_entries=2)

    inputs = [10, 10, [1, 2, 3], [1, 2, 3], {"a": 1}, {"a": 1}]
    for item in inputs:
        start = time.perf_counter()
        out = cached_service.execute(item)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"in={item!r} out={out!r} time_ms={elapsed:.2f}")
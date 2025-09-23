import time
from typing import Any, Dict

class ProcessorInterface:
    def process(self, data: Any) -> Any:
        raise NotImplementedError

class SimpleProcessor(ProcessorInterface):
    def process(self, data: Any) -> str:
        time.sleep(0.05)
        return f"processed:{data}"

class WrapperBase(ProcessorInterface):
    def __init__(self, inner: ProcessorInterface):
        if not hasattr(inner, "process") or not callable(inner.process):
            raise TypeError("inner must implement process")
        self._inner = inner
    def process(self, data: Any) -> Any:
        return self._inner.process(data)

class LoggingWrapper(WrapperBase):
    def __init__(self, inner: ProcessorInterface, enabled: bool = True):
        super().__init__(inner)
        self.enabled = enabled
    def process(self, data: Any) -> Any:
        if not self.enabled:
            return super().process(data)
        start = time.time()
        print(f"[LOG] start {data}")
        try:
            result = super().process(data)
        except Exception as e:
            print(f"[LOG] error {e}")
            raise
        print(f"[LOG] done {(time.time()-start)*1000:.1f}ms -> {result}")
        return result

class CacheWrapper(WrapperBase):
    def __init__(self, inner: ProcessorInterface, max_entries: int = 50):
        super().__init__(inner)
        self._cache: Dict[Any, Any] = {}
        self._max = max_entries
    def process(self, data: Any) -> Any:
        if data in self._cache:
            print(f"[CACHE] hit {data}")
            return self._cache[data]
        result = super().process(data)
        if len(self._cache) >= self._max:
            self._cache.pop(next(iter(self._cache)))
        self._cache[data] = result
        print(f"[CACHE] store {data}")
        return result

if __name__ == "__main__":
    base = SimpleProcessor()
    cached = CacheWrapper(base, max_entries=2)
    logged = LoggingWrapper(cached)
    inputs = ["alpha", "beta", "alpha", "gamma", "beta"]
    for item in inputs:
        try:
            output = logged.process(item)
            print("OUT>", output)
        except Exception as exc:
            print("Unhandled error:", exc)
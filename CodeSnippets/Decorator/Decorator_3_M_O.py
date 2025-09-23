from abc import ABC, abstractmethod
import time

class ServiceInterface(ABC):
    @abstractmethod
    def process(self, value):
        pass

class CoreService(ServiceInterface):
    def process(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("value must be a number")
        if value < 0:
            raise ValueError("negative values not allowed")
        time.sleep(0.08)
        return value * 2

class WrapperBase(ServiceInterface):
    def __init__(self, service):
        if not isinstance(service, ServiceInterface):
            raise TypeError("service must implement ServiceInterface")
        self._service = service
    def process(self, value):
        return self._service.process(value)

class LoggingWrapper(WrapperBase):
    def process(self, value):
        start = time.time()
        try:
            result = super().process(value)
            elapsed = time.time() - start
            print(f"[LOG] input={value} result={result} time={elapsed:.4f}s")
            return result
        except Exception as exc:
            elapsed = time.time() - start
            print(f"[ERROR] input={value} error={exc} time={elapsed:.4f}s")
            raise

class CacheWrapper(WrapperBase):
    def __init__(self, service, maxsize=64):
        super().__init__(service)
        self._cache = {}
        self._max = maxsize
    def process(self, value):
        key = value
        if key in self._cache:
            print(f"[CACHE HIT] key={key}")
            return self._cache[key]
        result = super().process(value)
        if len(self._cache) >= self._max:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = result
        print(f"[CACHE STORE] key={key}")
        return result

if __name__ == "__main__":
    core = CoreService()
    stacked = LoggingWrapper(CacheWrapper(core))
    inputs = [5, 5, 3, -2, 3]
    for v in inputs:
        try:
            out = stacked.process(v)
            print(f"Output: {out}")
        except Exception as e:
            print(f"Handled error for input {v}: {e}")
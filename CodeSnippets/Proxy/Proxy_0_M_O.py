from abc import ABC, abstractmethod
import time

class ServiceInterface(ABC):
    @abstractmethod
    def fetch(self, resource, credentials):
        pass

class RealService(ServiceInterface):
    def __init__(self):
        self._ready = True

    def fetch(self, resource, credentials=None):
        if not resource or not isinstance(resource, str):
            raise ValueError("Resource must be a non-empty string")
        time.sleep(1)  # simulate expensive operation
        return f"Contents of {resource}"

class ServiceGuard(ServiceInterface):
    def __init__(self, allowed_tokens=None):
        self._allowed = set(allowed_tokens or [])
        self._delegate = None
        self._cache = {}

    def _ensure_delegate(self):
        if self._delegate is None:
            self._delegate = RealService()

    def fetch(self, resource, credentials=None):
        if credentials not in self._allowed:
            raise PermissionError("Access denied: invalid credentials")
        if resource in self._cache:
            print(f"[cache] returning cached result for '{resource}'")
            return self._cache[resource]
        try:
            self._ensure_delegate()
            result = self._delegate.fetch(resource, credentials)
        except Exception as exc:
            raise RuntimeError("Failed to retrieve resource") from exc
        self._cache[resource] = result
        print(f"[fetch] retrieved and cached '{resource}'")
        return result

if __name__ == "__main__":
    guard = ServiceGuard(allowed_tokens={"token123"})
    try:
        guard.fetch("alpha", credentials="badtoken")
    except Exception as e:
        print("Error:", e)

    start = time.perf_counter()
    print(guard.fetch("alpha", credentials="token123"))
    mid = time.perf_counter()
    print(f"First call took {mid - start:.3f}s")

    print(guard.fetch("alpha", credentials="token123"))
    end = time.perf_counter()
    print(f"Second call took {end - mid:.3f}s")
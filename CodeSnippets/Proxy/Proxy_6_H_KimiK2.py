import time
from typing import Optional, Any
import threading

class Resource:
    def request(self, key: str) -> Any:
        raise NotImplementedError

class SlowRemote(Resource):
    def __init__(self):
        self._data = {"gold": 100, "silver": 200, "bronze": 300}

    def request(self, key: str) -> Any:
        time.sleep(1)
        return self._data.get(key)

class CachedGateway(Resource):
    def __init__(self, remote: Resource, ttl: float = 5.0):
        self._remote = remote
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = threading.RLock()
        self._ttl = ttl

    def request(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                value, ts = self._cache[key]
                if time.time() - ts < self._ttl:
                    return value
            value = self._remote.request(key)
            if value is not None:
                self._cache[key] = (value, time.time())
            return value

class SecuredWrapper(Resource):
    def __init__(self, wrapped: Resource, allowed: set[str]):
        self._wrapped = wrapped
        self._allowed = allowed

    def request(self, key: str) -> Any:
        if key not in self._allowed:
            raise PermissionError("Unauthorized access")
        return self._wrapped.request(key)

if __name__ == "__main__":
    remote = SlowRemote()
    gateway = CachedGateway(remote, ttl=2.0)
    secured = SecuredWrapper(gateway, allowed={"gold", "silver"})

    for k in ("gold", "silver", "bronze"):
        try:
            start = time.time()
            v = secured.request(k)
            print(f"{k}: {v} ({time.time()-start:.2f}s)")
        except Exception as e:
            print(f"{k}: {e}")
import time
import threading
import abc
from typing import Dict, Tuple, Optional

class DataFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch(self, resource_id: str) -> str:
        pass

class RemoteFetcher(DataFetcher):
    def __init__(self, storage: Dict[str, str]):
        self._storage = storage

    def fetch(self, resource_id: str) -> str:
        time.sleep(0.5)
        if resource_id not in self._storage:
            raise KeyError(f"Resource '{resource_id}' not found")
        return self._storage[resource_id]

class CachingFetcher(DataFetcher):
    def __init__(self, wrapped: DataFetcher, ttl: float = 5.0):
        self._wrapped = wrapped
        self._ttl = ttl
        self._cache: Dict[str, Tuple[str, float]] = {}
        self._lock = threading.Lock()

    def fetch(self, resource_id: str) -> str:
        now = time.time()
        stale: Optional[Tuple[str, float]] = None
        with self._lock:
            entry = self._cache.get(resource_id)
            if entry:
                value, expiry = entry
                if expiry >= now:
                    return value
                stale = (value, expiry)
        try:
            result = self._wrapped.fetch(resource_id)
        except Exception:
            if stale:
                with self._lock:
                    self._cache[resource_id] = (stale[0], time.time() + self._ttl)
                return stale[0]
            raise
        with self._lock:
            self._cache[resource_id] = (result, time.time() + self._ttl)
        return result

if __name__ == "__main__":
    storage = {"item1": "Data for item 1", "item2": "Data for item 2"}
    remote = RemoteFetcher(storage)
    cached = CachingFetcher(remote, ttl=2.0)

    start = time.time()
    print(cached.fetch("item1"))
    print("took", round(time.time() - start, 3), "s")

    start = time.time()
    print(cached.fetch("item1"))
    print("took", round(time.time() - start, 3), "s")

    time.sleep(2.1)
    start = time.time()
    print(cached.fetch("item1"))
    print("took", round(time.time() - start, 3), "s")

    try:
        print(cached.fetch("missing"))
    except KeyError as e:
        print("Error:", e)
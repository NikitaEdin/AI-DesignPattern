import abc
import threading
import time
import random
from typing import Any, Dict, Tuple

class AccessDenied(Exception):
    pass

class ResourceUnavailable(Exception):
    pass

class ResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch(self, key: str, role: str) -> Any:
        pass

class HeavyResource(ResourceInterface):
    def __init__(self):
        time.sleep(0.2)
        self._start = time.time()
        self._counter = 0

    def fetch(self, key: str, role: str) -> Dict[str, Any]:
        self._counter += 1
        if random.random() < 0.25:
            raise RuntimeError("transient error")
        time.sleep(0.05)
        return {"key": key, "value": f"value_for_{key}", "fetched_at": time.time(), "count": self._counter}

class ResourceMediator(ResourceInterface):
    def __init__(self, allowed_roles=None, cache_ttl=2.0, init_retries=3, call_retries=3, retry_backoff=0.1):
        self._allowed_roles = set(allowed_roles or {"admin", "user"})
        self._cache_ttl = float(cache_ttl)
        self._init_retries = int(init_retries)
        self._call_retries = int(call_retries)
        self._retry_backoff = float(retry_backoff)
        self._real = None
        self._lock = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = {"hits": 0, "misses": 0, "init_failures": 0}

    def _ensure_real(self):
        if self._real is not None:
            return
        with self._lock:
            if self._real is not None:
                return
            last_exc = None
            for attempt in range(1, self._init_retries + 1):
                try:
                    self._real = HeavyResource()
                    return
                except Exception as e:
                    last_exc = e
                    self._metrics["init_failures"] += 1
                    time.sleep(self._retry_backoff * attempt)
            raise ResourceUnavailable(f"Failed to initialize resource after {self._init_retries} attempts") from last_exc

    def _get_cached(self, key: str):
        entry = self._cache.get(key)
        if not entry:
            return None
        value, expiry = entry
        if time.time() > expiry:
            with self._lock:
                if key in self._cache and self._cache[key][1] <= time.time():
                    del self._cache[key]
            return None
        return value

    def _set_cache(self, key: str, value: Any):
        expiry = time.time() + self._cache_ttl
        with self._lock:
            self._cache[key] = (value, expiry)

    def fetch(self, key: str, role: str) -> Any:
        if role not in self._allowed_roles:
            raise AccessDenied(f"role '{role}' not allowed")
        cached = self._get_cached(key)
        if cached is not None:
            self._metrics["hits"] += 1
            return {"cached": True, "data": cached}
        self._metrics["misses"] += 1
        self._ensure_real()
        last_exc = None
        for attempt in range(1, self._call_retries + 1):
            try:
                result = self._real.fetch(key, role)
                self._set_cache(key, result)
                return {"cached": False, "data": result}
            except RuntimeError as e:
                last_exc = e
                time.sleep(self._retry_backoff * attempt)
            except Exception as e:
                raise
        raise ResourceUnavailable("call failed after retries") from last_exc

    def stats(self):
        with self._lock:
            return dict(self._metrics)

if __name__ == "__main__":
    mediator = ResourceMediator(allowed_roles={"admin", "user"}, cache_ttl=1.0, init_retries=2, call_retries=4, retry_backoff=0.05)

    def worker(name, key, role):
        try:
            res = mediator.fetch(key, role)
            print(f"{name} got: {res}")
        except AccessDenied as e:
            print(f"{name} access denied: {e}")
        except ResourceUnavailable as e:
            print(f"{name} unavailable: {e}")
        except Exception as e:
            print(f"{name} error: {e}")

    threads = []
    roles = ["admin", "user", "guest"]
    for i in range(8):
        t = threading.Thread(target=worker, args=(f"worker{i}", f"item{(i%3)}", random.choice(roles)))
        threads.append(t)
        t.start()
        time.sleep(0.03)

    for t in threads:
        t.join()

    print("Final stats:", mediator.stats())
    print("Cache content snapshot:")
    for k, v in mediator._cache.items():
        print(k, v)
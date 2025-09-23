import threading
import time
import random
from abc import ABC, abstractmethod
from collections import OrderedDict

class ServiceInterface(ABC):
    @abstractmethod
    def perform(self, user: str, request: str) -> str:
        pass

class ServiceUnavailable(Exception):
    pass

class AccessDenied(Exception):
    pass

class HeavyWorker(ServiceInterface):
    def __init__(self, startup_delay: float = 0.5):
        time.sleep(startup_delay)
        self._id = random.randint(1000, 9999)

    def perform(self, user: str, request: str) -> str:
        if request == "fail":
            raise ServiceUnavailable("Simulated failure")
        time.sleep(0.2 + random.random() * 0.3)
        return f"result:{self._id}:{request}"

class Gatekeeper(ServiceInterface):
    def __init__(self, allowed_users=None, cache_capacity: int = 64, ttl: float = 10.0):
        self._allowed = set(allowed_users or [])
        self._cache = OrderedDict()
        self._cache_meta = {}
        self._cache_capacity = max(1, cache_capacity)
        self._ttl = max(0.0, ttl)
        self._real = None
        self._lock = threading.RLock()
        self._usage = {}
        self._failover = lambda u, r: f"fallback:{u}:{r}"
        self._started = False

    def _ensure_real(self):
        if self._real is None:
            with self._lock:
                if self._real is None:
                    self._real = HeavyWorker()
                    self._started = True

    def _is_allowed(self, user: str) -> bool:
        return not self._allowed or user in self._allowed

    def _make_key(self, user: str, request: str) -> str:
        return f"{user}|{request}"

    def _evict_if_needed(self):
        while len(self._cache) > self._cache_capacity:
            self._cache.popitem(last=False)

    def _prune_expired(self):
        now = time.time()
        keys_to_delete = [k for k, t in self._cache_meta.items() if now - t > self._ttl]
        for k in keys_to_delete:
            self._cache_meta.pop(k, None)
            self._cache.pop(k, None)

    def perform(self, user: str, request: str) -> str:
        if not isinstance(user, str) or not isinstance(request, str):
            raise TypeError("user and request must be strings")
        if not self._is_allowed(user):
            raise AccessDenied(f"user '{user}' not permitted")
        key = self._make_key(user, request)
        with self._lock:
            self._prune_expired()
            if key in self._cache:
                value = self._cache.pop(key)
                self._cache[key] = value
                self._usage[key] = self._usage.get(key, 0) + 1
                return value
        try:
            self._ensure_real()
            result = self._real.perform(user, request)
        except Exception:
            return self._failover(user, request)
        with self._lock:
            if key in self._cache:
                self._cache.pop(key)
            self._cache[key] = result
            self._cache_meta[key] = time.time()
            self._evict_if_needed()
            self._usage[key] = self._usage.get(key, 0) + 1
        return result

    def stats(self):
        with self._lock:
            return {
                "started": self._started,
                "cache_size": len(self._cache),
                "cache_capacity": self._cache_capacity,
                "ttl": self._ttl,
                "usage_samples": dict(list(self._usage.items())[:10])
            }

    def clear_cache(self):
        with self._lock:
            self._cache.clear()
            self._cache_meta.clear()

if __name__ == "__main__":
    gate = Gatekeeper(allowed_users={"alice", "bob"}, cache_capacity=8, ttl=5.0)
    requests = [("alice", "task1"), ("bob", "task1"), ("alice", "task1"), ("eve", "task2"), ("bob", "fail")]
    results = []
    def worker(u, r, out):
        try:
            out.append((u, r, gate.perform(u, r)))
        except Exception as e:
            out.append((u, r, f"error:{type(e).__name__}:{e}"))
    threads = []
    for u, r in requests:
        t = threading.Thread(target=worker, args=(u, r, results))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for entry in results:
        print(entry)
    print("STATS:", gate.stats())
    gate.clear_cache()
    print("CLEARED:", gate.stats())
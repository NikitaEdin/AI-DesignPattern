from abc import ABC, abstractmethod
import threading
import time
import random
import concurrent.futures

class ServiceInterface(ABC):
    @abstractmethod
    def fetch(self, resource_id: str) -> str:
        pass

class RealService(ServiceInterface):
    def __init__(self):
        time.sleep(0.2)
        if random.random() < 0.1:
            raise RuntimeError("Initialization failure")
        self._startup = time.time()

    def fetch(self, resource_id: str) -> str:
        time.sleep(0.1)
        return f"data for {resource_id} (served at {time.time():.3f})"

class ServiceGateway(ServiceInterface):
    def __init__(self, user_role: str = "guest", max_retries: int = 3, cache_ttl: float = 2.0):
        self._role = user_role
        self._max_retries = max_retries
        self._cache_ttl = cache_ttl
        self._real = None
        self._lock = threading.RLock()
        self._cache = {}
        self._metrics = {"hits": 0, "misses": 0, "init_retries": 0, "errors": 0}

    def _ensure_real(self):
        if self._real is not None:
            return
        with self._lock:
            if self._real is not None:
                return
            attempts = 0
            while attempts < self._max_retries:
                try:
                    self._real = RealService()
                    return
                except Exception:
                    attempts += 1
                    self._metrics["init_retries"] += 1
                    time.sleep(0.05 * attempts)
            self._metrics["errors"] += 1
            raise RuntimeError("Unable to initialize backend after retries")

    def _check_access(self, resource_id: str):
        if resource_id.startswith("secret") and self._role != "admin":
            raise PermissionError("Access denied for resource")

    def _get_cached(self, resource_id: str):
        entry = self._cache.get(resource_id)
        if entry:
            value, ts = entry
            if time.time() - ts < self._cache_ttl:
                self._metrics["hits"] += 1
                return value
            else:
                self._cache.pop(resource_id, None)
        self._metrics["misses"] += 1
        return None

    def fetch(self, resource_id: str) -> str:
        self._check_access(resource_id)
        cached = self._get_cached(resource_id)
        if cached is not None:
            return cached
        self._ensure_real()
        try:
            with self._lock:
                cached = self._get_cached(resource_id)
                if cached is not None:
                    return cached
                result = self._real.fetch(resource_id)
                self._cache[resource_id] = (result, time.time())
                return result
        except Exception as e:
            self._metrics["errors"] += 1
            raise e

    def invalidate(self, resource_id: str):
        with self._lock:
            self._cache.pop(resource_id, None)

    def stats(self):
        with self._lock:
            return dict(self._metrics)

if __name__ == "__main__":
    gateway = ServiceGateway(user_role="guest", cache_ttl=1.5)
    print(gateway.fetch("public/1"))
    print(gateway.fetch("public/1"))
    try:
        print(gateway.fetch("secret/42"))
    except Exception as e:
        print("Error:", e)
    admin_gateway = ServiceGateway(user_role="admin", cache_ttl=3.0)
    ids = [f"item/{i%3}" for i in range(8)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(admin_gateway.fetch, rid) for rid in ids]
        for f in concurrent.futures.as_completed(futures):
            try:
                print(f.result())
            except Exception as e:
                print("Fetch error:", e)
    print("Guest stats:", gateway.stats())
    print("Admin stats:", admin_gateway.stats())
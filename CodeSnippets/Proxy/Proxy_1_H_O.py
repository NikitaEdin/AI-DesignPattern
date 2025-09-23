import time
import threading
import hashlib
import logging
from abc import ABCMeta, abstractmethod

logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")

class AccessDeniedError(Exception):
    pass

class ServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class RealService(ServiceInterface):
    def __init__(self):
        time.sleep(0.3)
        self._created_at = time.time()
    def execute(self, payload):
        time.sleep(0.1)
        return {"result": f"handled:{payload}", "timestamp": time.time(), "created": self._created_at}

class ServiceGuard(ServiceInterface):
    def __init__(self, user, allowed_roles=None, cache_enabled=True):
        self._user = user or {}
        self._allowed_roles = set(allowed_roles or {"admin", "user"})
        self._cache_enabled = bool(cache_enabled)
        self._real = None
        self._lock = threading.RLock()
        self._cache = {}
        self._logger = logging.getLogger(self.__class__.__name__)
    def _check_access(self):
        role = self._user.get("role")
        if role not in self._allowed_roles:
            raise AccessDeniedError(f"role '{role}' not permitted")
    def _cache_key(self, args, kwargs):
        h = hashlib.sha256()
        h.update(repr(args).encode())
        h.update(repr(sorted(kwargs.items())).encode())
        return h.hexdigest()
    def _get_real(self):
        if self._real is None:
            with self._lock:
                if self._real is None:
                    self._logger.info("Initializing backend service")
                    self._real = RealService()
        return self._real
    def execute(self, *args, **kwargs):
        self._check_access()
        key = None
        if self._cache_enabled:
            key = self._cache_key(args, kwargs)
            with self._lock:
                if key in self._cache:
                    self._logger.info("Cache hit")
                    return self._cache[key]
        try:
            real = self._get_real()
            result = real.execute(*args, **kwargs)
            if self._cache_enabled:
                with self._lock:
                    self._cache[key] = result
            return result
        except Exception:
            self._logger.exception("Execution failed")
            raise
    def invalidate_cache(self, predicate=None):
        with self._lock:
            if predicate is None:
                self._cache.clear()
                return 0
            removed = 0
            for k in list(self._cache.keys()):
                if predicate(k, self._cache[k]):
                    del self._cache[k]
                    removed += 1
            return removed

if __name__ == "__main__":
    admin = {"name": "Alice", "role": "admin"}
    guest = {"name": "Eve", "role": "guest"}

    service_for_admin = ServiceGuard(admin, allowed_roles={"admin"})
    out1 = service_for_admin.execute("task-1")
    print("First call:", out1)
    out2 = service_for_admin.execute("task-1")
    print("Second call (cached):", out2)
    removed = service_for_admin.invalidate_cache()
    print("Cache cleared, removed entries:", removed)
    out3 = service_for_admin.execute("task-1")
    print("After clear:", out3)

    service_for_guest = ServiceGuard(guest, allowed_roles={"admin", "user"})
    try:
        service_for_guest.execute("task-X")
    except AccessDeniedError as e:
        print("Access denied as expected for guest:", e)

    def thread_job(svc, name):
        print(name, svc.execute("concurrent"))

    svc = ServiceGuard(admin)
    threads = [threading.Thread(target=thread_job, args=(svc, f"T{i}")) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
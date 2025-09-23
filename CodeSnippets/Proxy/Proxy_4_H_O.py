import threading
import time
import weakref
import json
import random
from collections import OrderedDict
from abc import ABC, abstractmethod

class ServiceUnavailableError(RuntimeError):
    pass

class AccessDeniedError(PermissionError):
    pass

class ServiceInterface(ABC):
    @abstractmethod
    def perform(self, action, payload, role="guest"):
        pass

class HeavyService(ServiceInterface):
    def __init__(self, startup_fail_rate=0.2):
        # simulate expensive startup that may fail
        time.sleep(0.05)
        if random.random() < startup_fail_rate:
            raise RuntimeError("failed to initialize heavy resource")
    def perform(self, action, payload, role="guest"):
        # deterministic-ish result based on content
        key = json.dumps({"action": action, "payload": payload}, sort_keys=True, default=str)
        return f"result:{hash(key)%10000}"

class LRUCache:
    def __init__(self, max_size=128):
        self.max_size = max_size
        self._data = OrderedDict()
        self._lock = threading.RLock()
        self._MISSING = object()
    def get(self, key):
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
                return self._data[key]
            return self._MISSING
    def set(self, key, value):
        with self._lock:
            self._data[key] = value
            self._data.move_to_end(key)
            if len(self._data) > self.max_size:
                self._data.popitem(last=False)
    def missing_sentinel(self):
        return self._MISSING

class ServiceGuard(ServiceInterface):
    def __init__(self, factory=lambda: HeavyService(), retries=3, backoff=0.1):
        self._factory = factory
        self._weak_real = None
        self._lock = threading.RLock()
        self._retries = retries
        self._backoff = backoff
        self._cache = LRUCache(max_size=256)
        self._access = {"admin": {"*"}, "user": {"read"}, "guest": set()}
    def _canonical_key(self, action, payload, role):
        payload_repr = json.dumps(payload, sort_keys=True, default=str)
        return f"{role}|{action}|{payload_repr}"
    def _ensure_real(self):
        real = self._weak_real() if self._weak_real else None
        if real:
            return real
        with self._lock:
            real = self._weak_real() if self._weak_real else None
            if real:
                return real
            last_exc = None
            for attempt in range(1, self._retries + 1):
                try:
                    real_obj = self._factory()
                    self._weak_real = weakref.ref(real_obj)
                    return real_obj
                except Exception as e:
                    last_exc = e
                    time.sleep(self._backoff * attempt)
            raise ServiceUnavailableError("unable to initialize service") from last_exc
    def _check_access(self, action, role):
        allowed = self._access.get(role, set())
        return ("*" in allowed) or (action in allowed)
    def perform(self, action, payload, role="guest"):
        if not self._check_access(action, role):
            raise AccessDeniedError(f"role '{role}' not allowed to perform '{action}'")
        key = self._canonical_key(action, payload, role)
        miss = self._cache.missing_sentinel()
        cached = self._cache.get(key)
        if cached is not miss:
            return cached
        # obtain and use real; if perform fails, try one reinit then fail
        real = self._ensure_real()
        try:
            result = real.perform(action, payload, role=role)
        except Exception as e:
            # drop and retry once with a fresh instance
            with self._lock:
                self._weak_real = None
            try:
                real = self._ensure_real()
                result = real.perform(action, payload, role=role)
            except Exception as e2:
                raise ServiceUnavailableError("remote operation failed") from e2
        self._cache.set(key, result)
        return result

if __name__ == "__main__":
    guard = ServiceGuard(factory=lambda: HeavyService(startup_fail_rate=0.3), retries=4, backoff=0.05)
    # single-threaded usage
    print(guard.perform("read", {"id": 1}, role="user"))
    # cached hit
    print(guard.perform("read", {"id": 1}, role="user"))
    # access denied
    try:
        print(guard.perform("write", {"id": 2}, role="user"))
    except Exception as e:
        print("expected:", type(e).__name__, e)
    # concurrent usage
    def worker(i):
        try:
            res = guard.perform("read", {"id": i % 3}, role="user")
            print(f"worker {i}: {res}")
        except Exception as e:
            print(f"worker {i} error:", e)
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
from abc import ABC, abstractmethod
from threading import Lock, Thread
from time import sleep, time
from typing import Any, Dict, Optional, Tuple


class ServiceInterface(ABC):
    @abstractmethod
    def perform_operation(self, payload: Any) -> Any:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass


class HeavyWorker(ServiceInterface):
    def __init__(self):
        sleep(0.2)
        self.started_at = time()

    def perform_operation(self, payload: Any) -> Any:
        if payload is None:
            raise ValueError("payload must not be None")
        sleep(0.1)
        return {"result": f"processed:{payload}", "time": time()}

    def get_status(self) -> str:
        return f"ready since {self.started_at}"


class ServiceGuard(ServiceInterface):
    def __init__(self, allowed_users: Optional[set] = None, cache_size: int = 16, max_calls: int = 100):
        self._allowed = set(allowed_users or [])
        self._cache_size = max(1, int(cache_size))
        self._max_calls = max(1, int(max_calls))
        self._real: Optional[ServiceInterface] = None
        self._lock = Lock()
        self._cache: Dict[Any, Tuple[Any, float]] = {}
        self._call_count = 0
        self._revoked = False

    def authorize(self, user: str):
        with self._lock:
            self._allowed.add(user)

    def deauthorize(self, user: str):
        with self._lock:
            self._allowed.discard(user)

    def revoke(self):
        with self._lock:
            self._real = None
            self._revoked = True
            self._cache.clear()
            self._call_count = 0

    def _ensure_real(self) -> ServiceInterface:
        if self._revoked:
            raise RuntimeError("service access revoked")
        if self._real is None:
            with self._lock:
                if self._real is None:
                    self._real = HeavyWorker()
        return self._real

    def _check_limits(self):
        with self._lock:
            if self._call_count >= self._max_calls:
                raise RuntimeError("call limit exceeded")
            self._call_count += 1

    def _get_cached(self, key: Any) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if entry:
                value, ts = entry
                return value
            return None

    def _set_cached(self, key: Any, value: Any):
        with self._lock:
            if key in self._cache:
                self._cache[key] = (value, time())
                return
            if len(self._cache) >= self._cache_size:
                oldest = min(self._cache.items(), key=lambda kv: kv[1][1])[0]
                del self._cache[oldest]
            self._cache[key] = (value, time())

    def perform_operation(self, payload: Any, user: Optional[str] = None) -> Any:
        if user is None:
            raise ValueError("user is required")
        if user not in self._allowed:
            raise PermissionError("user not authorized")
        if payload is None:
            raise ValueError("payload must not be None")
        cache_key = (repr(payload), user)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return {"cached": True, "value": cached}
        self._check_limits()
        try:
            real = self._ensure_real()
            result = real.perform_operation(payload)
            self._set_cached(cache_key, result)
            return {"cached": False, "value": result}
        except Exception as exc:
            return {"error": str(exc)}

    def get_status(self) -> str:
        try:
            real = self._ensure_real()
            return real.get_status()
        except Exception:
            return "unavailable"

    def __getattr__(self, item):
        real = None
        try:
            real = self._ensure_real()
        except Exception:
            raise AttributeError(item)
        return getattr(real, item)


if __name__ == "__main__":
    guard = ServiceGuard(allowed_users={"alice"}, cache_size=4, max_calls=10)
    print(guard.get_status())
    print(guard.perform_operation("task1", user="alice"))
    print(guard.perform_operation("task1", user="alice"))
    try:
        print(guard.perform_operation("task2", user="bob"))
    except Exception as e:
        print("expected:", type(e).__name__, e)
    def worker_call(name, payload):
        try:
            print(name, guard.perform_operation(payload, user="alice"))
        except Exception as e:
            print(name, "err", e)
    threads = [Thread(target=worker_call, args=(f"t{i}", f"job{i}")) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    guard.revoke()
    try:
        print(guard.get_status())
    except Exception as e:
        print("after revoke:", e)
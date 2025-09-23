import time
import threading
import abc
from typing import Optional, Tuple, Dict, Set


class AccessDeniedError(Exception):
    pass


class ServiceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch(self, resource: str, user: str) -> str:
        pass


class HeavyService(ServiceInterface):
    def __init__(self):
        time.sleep(0.2)
        self._start = time.time()

    def fetch(self, resource: str, user: str) -> str:
        time.sleep(0.05)
        return f"data:{resource}@{user}:{time.time():.4f}"


class ServiceGate(ServiceInterface):
    def __init__(self, allowed_users: Optional[Set[str]] = None, cache_ttl: float = 2.0):
        self._allowed: Set[str] = set(allowed_users or [])
        self._ttl = float(cache_ttl)
        self._real: Optional[HeavyService] = None
        self._cache: Dict[str, Tuple[float, str]] = {}
        self._lock = threading.RLock()
        self._enabled = True

    def add_user(self, user: str) -> None:
        with self._lock:
            self._allowed.add(user)

    def remove_user(self, user: str) -> None:
        with self._lock:
            self._allowed.discard(user)

    def enable(self) -> None:
        with self._lock:
            self._enabled = True

    def disable(self) -> None:
        with self._lock:
            self._enabled = False

    def invalidate_cache(self, resource: Optional[str] = None) -> None:
        with self._lock:
            if resource is None:
                self._cache.clear()
            else:
                self._cache.pop(resource, None)

    def _authorize(self, user: str) -> None:
        if user not in self._allowed:
            raise AccessDeniedError(f"user '{user}' is not authorized")

    def _get_real(self) -> HeavyService:
        if self._real is None:
            self._real = HeavyService()
        return self._real

    def fetch(self, resource: str, user: str) -> str:
        if not self._enabled:
            raise AccessDeniedError("service is disabled")
        self._authorize(user)
        now = time.time()
        with self._lock:
            entry = self._cache.get(resource)
            if entry:
                ts, val = entry
                if now - ts < self._ttl:
                    return val
            real = self._get_real()
        result = real.fetch(resource, user)
        with self._lock:
            self._cache[resource] = (time.time(), result)
        return result


if __name__ == "__main__":
    gate = ServiceGate(allowed_users={"alice", "bob"}, cache_ttl=1.0)

    def attempt(resource, user):
        try:
            return gate.fetch(resource, user)
        except AccessDeniedError as e:
            return f"ERROR: {e}"

    print(attempt("file1", "alice"))
    print(attempt("file1", "alice"))
    time.sleep(1.1)
    print(attempt("file1", "alice"))
    print(attempt("file2", "charlie"))
    gate.add_user("charlie")
    print(attempt("file2", "charlie"))
    gate.disable()
    print(attempt("file1", "alice"))
    gate.enable()
    gate.invalidate_cache()
    print(attempt("file1", "alice"))
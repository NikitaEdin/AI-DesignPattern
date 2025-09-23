import abc
import threading
import time
from typing import Optional, Dict, Tuple


class ServiceInterface(abc.ABC):
    @abc.abstractmethod
    def perform(self, task: str, timeout: Optional[float] = None, refresh: bool = False) -> str:
        pass


class OperationDenied(Exception):
    pass


class OperationTimedOut(Exception):
    pass


class RealWorker(ServiceInterface):
    def __init__(self):
        time.sleep(0.2)
        self._ready_at = time.time()

    def perform(self, task: str, timeout: Optional[float] = None, refresh: bool = False) -> str:
        start = time.time()
        duration = min(0.3 + len(task) * 0.01, 2.0)
        if timeout is not None and timeout < duration:
            raise OperationTimedOut(f"Task '{task}' exceeded timeout {timeout}s (needs ~{duration:.2f}s)")
        time.sleep(duration)
        finished = time.time()
        return f"Result({task}) generated at {finished:.3f}"


class AccessGateway(ServiceInterface):
    def __init__(self, token: Optional[str], allowed_tokens: Optional[Dict[str, str]] = None, cache_ttl: float = 5.0):
        self._token = token
        self._allowed_tokens = allowed_tokens or {}
        self._cache_ttl = max(0.0, float(cache_ttl))
        self._worker_lock = threading.Lock()
        self._worker: Optional[RealWorker] = None
        self._cache_lock = threading.Lock()
        self._cache: Dict[str, Tuple[str, float]] = {}

    def _is_authorized(self) -> bool:
        return self._token is not None and self._token in self._allowed_tokens

    def _ensure_worker(self) -> RealWorker:
        if self._worker is None:
            with self._worker_lock:
                if self._worker is None:
                    self._worker = RealWorker()
        return self._worker

    def _get_cached(self, task: str) -> Optional[str]:
        with self._cache_lock:
            entry = self._cache.get(task)
            if entry:
                result, expiry = entry
                if expiry >= time.time():
                    return result
                else:
                    del self._cache[task]
        return None

    def _set_cache(self, task: str, result: str) -> None:
        if self._cache_ttl <= 0:
            return
        with self._cache_lock:
            self._cache[task] = (result, time.time() + self._cache_ttl)

    def perform(self, task: str, timeout: Optional[float] = None, refresh: bool = False) -> str:
        if not self._is_authorized():
            raise OperationDenied("Token is missing or invalid.")

        if not refresh:
            cached = self._get_cached(task)
            if cached is not None:
                return f"Cached -> {cached}"

        worker = self._ensure_worker()
        result = worker.perform(task, timeout=timeout, refresh=refresh)
        self._set_cache(task, result)
        return f"Live -> {result}"

    def update_token(self, token: Optional[str]) -> None:
        with self._worker_lock:
            self._token = token

    def invalidate_cache(self, task: Optional[str] = None) -> None:
        with self._cache_lock:
            if task is None:
                self._cache.clear()
            else:
                self._cache.pop(task, None)


if __name__ == "__main__":
    allowed = {"alice-token": "alice", "bob-token": "bob"}
    gateway = AccessGateway(token="alice-token", allowed_tokens=allowed, cache_ttl=2.0)

    print(gateway.perform("compute-prime-1000"))
    print(gateway.perform("compute-prime-1000"))
    print(gateway.perform("compute-prime-1000", refresh=True))

    try:
        bad_gateway = AccessGateway(token=None, allowed_tokens=allowed)
        print(bad_gateway.perform("task"))
    except OperationDenied as e:
        print("Denied:", e)

    gateway.invalidate_cache("compute-prime-1000")
    print(gateway.perform("compute-prime-1000"))

    def worker_task(name: str):
        try:
            res = gateway.perform("concurrent-job", timeout=3.0)
            print(f"{name}: {res}")
        except Exception as exc:
            print(f"{name} error:", exc)

    threads = [threading.Thread(target=worker_task, args=(f"T{i}",)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
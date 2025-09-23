from abc import ABC, abstractmethod
import time
from typing import Dict, Tuple, Set


class ServiceInterface(ABC):
    @abstractmethod
    def fetch(self, resource_id: str) -> str:
        pass


class CoreService(ServiceInterface):
    def fetch(self, resource_id: str) -> str:
        time.sleep(1.0)
        return f"Fetched [{resource_id}] at {time.time()}"


class AccessGuard(ServiceInterface):
    def __init__(self, service: ServiceInterface, token: str, valid_tokens: Set[str], ttl: float = 5.0):
        if token not in valid_tokens:
            raise PermissionError("Invalid credential provided")
        self._service = service
        self._token = token
        self._valid_tokens = valid_tokens
        self._cache: Dict[str, Tuple[float, str]] = {}
        self._ttl = ttl

    def fetch(self, resource_id: str) -> str:
        if self._token not in self._valid_tokens:
            raise PermissionError("Credential revoked or invalid")
        now = time.time()
        cached = self._cache.get(resource_id)
        if cached:
            ts, data = cached
            if now - ts <= self._ttl:
                return data
        try:
            data = self._service.fetch(resource_id)
        except Exception as exc:
            raise RuntimeError("Underlying service failure") from exc
        self._cache[resource_id] = (now, data)
        return data


if __name__ == "__main__":
    valid = {"alpha-token", "beta-token"}
    core = CoreService()

    try:
        guard_bad = AccessGuard(core, token="bad", valid_tokens=valid)
    except PermissionError as e:
        print("Auth failed as expected:", e)

    guard = AccessGuard(core, token="alpha-token", valid_tokens=valid, ttl=3.0)
    start = time.time()
    print("First fetch:", guard.fetch("resource-1"), f"(t={time.time()-start:.2f}s)")
    start = time.time()
    print("Second fetch (cached):", guard.fetch("resource-1"), f"(t={time.time()-start:.2f}s)")
    time.sleep(4.0)
    start = time.time()
    print("Third fetch (after TTL):", guard.fetch("resource-1"), f"(t={time.time()-start:.2f}s)")
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

class AccessDeniedError(Exception):
    pass

class ServiceInterface(ABC):
    @abstractmethod
    def get_resource(self, identifier: str, user: str) -> Any:
        pass

class RealService(ServiceInterface):
    def get_resource(self, identifier: str, user: str) -> Dict[str, Any]:
        if not identifier:
            raise ValueError("Identifier must be provided")
        time.sleep(0.5)
        return {"id": identifier, "owner": "system", "data": f"Value for {identifier}", "fetched_by": user}

class ServiceController(ServiceInterface):
    def __init__(self, real_service: ServiceInterface, allowed_users=None, cache_ttl: float = 5.0):
        self._real = real_service
        self._allowed = set(allowed_users or [])
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._ttl = float(cache_ttl)

    def _is_allowed(self, user: str) -> bool:
        return user in self._allowed

    def _get_from_cache(self, identifier: str):
        entry = self._cache.get(identifier)
        if not entry:
            return None
        ts, value = entry
        if time.time() - ts > self._ttl:
            del self._cache[identifier]
            return None
        return value

    def get_resource(self, identifier: str, user: str) -> Any:
        if not self._is_allowed(user):
            raise AccessDeniedError(f"User '{user}' is not authorized")
        cached = self._get_from_cache(identifier)
        if cached is not None:
            return {"cached": True, "payload": cached}
        try:
            payload = self._real.get_resource(identifier, user)
        except Exception as e:
            raise RuntimeError("Failed to fetch resource") from e
        self._cache[identifier] = (time.time(), payload)
        return {"cached": False, "payload": payload}

if __name__ == "__main__":
    real = RealService()
    controller = ServiceController(real, allowed_users=["alice", "bob"], cache_ttl=2.0)

    users = ["alice", "eve", "alice"]
    ids = ["item1", "item1", "item1"]
    for user, ident in zip(users, ids):
        try:
            result = controller.get_resource(ident, user)
            print(f"{user} -> {result}")
        except AccessDeniedError as ade:
            print(f"{user} -> access denied: {ade}")
        except Exception as exc:
            print(f"{user} -> error: {exc}")

    time.sleep(3)
    try:
        print("After TTL:", controller.get_resource("item1", "alice"))
    except Exception as exc:
        print("Error after TTL:", exc)
import time
from abc import ABC, abstractmethod

class DataServiceInterface(ABC):
    @abstractmethod
    def fetch(self, key: str, user_token: str = None) -> str:
        pass

class RemoteDataService(DataServiceInterface):
    def fetch(self, key: str, user_token: str = None) -> str:
        time.sleep(0.8)
        if not key:
            raise ValueError("Empty key")
        if key == "corrupt":
            raise RuntimeError("Remote data corrupted")
        return f"remote:{key}"

class AccessControlledService(DataServiceInterface):
    def __init__(self, real_service: DataServiceInterface, allowed_tokens=None):
        self._real = real_service
        self._allowed = set(allowed_tokens or ())
        self._cache = {}

    def register_token(self, token: str):
        self._allowed.add(token)

    def revoke_token(self, token: str):
        self._allowed.discard(token)

    def _is_allowed(self, token: str) -> bool:
        return bool(token) and token in self._allowed

    def fetch(self, key: str, user_token: str = None) -> str:
        if not self._is_allowed(user_token):
            raise PermissionError("Access denied")
        cache_key = (key, user_token)
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            result = self._real.fetch(key, user_token)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve '{key}': {e}") from e
        self._cache[cache_key] = result
        return result

if __name__ == "__main__":
    backend = RemoteDataService()
    gateway = AccessControlledService(backend, allowed_tokens={"alice-token"})
    try:
        print(gateway.fetch("item42", user_token="alice-token"))
        print(gateway.fetch("item42", user_token="alice-token"))
        try:
            print(gateway.fetch("item42", user_token="bob-token"))
        except PermissionError as pe:
            print("PermissionError:", pe)
        gateway.register_token("bob-token")
        print(gateway.fetch("item42", user_token="bob-token"))
        try:
            print(gateway.fetch("corrupt", user_token="alice-token"))
        except RuntimeError as re:
            print("RuntimeError:", re)
    except Exception as exc:
        print("Unexpected error:", exc)
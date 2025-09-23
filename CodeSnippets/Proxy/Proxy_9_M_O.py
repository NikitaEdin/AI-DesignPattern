import time
from typing import Optional

class ResourceInterface:
    def fetch(self) -> str:
        raise NotImplementedError

class RealResource(ResourceInterface):
    def __init__(self, identifier: str):
        if not identifier or not isinstance(identifier, str):
            raise ValueError("Invalid resource identifier")
        self.identifier = identifier
        self._data: Optional[str] = None

    def _load(self) -> str:
        time.sleep(0.5)
        return f"Data for '{self.identifier}' loaded at {time.time()}"

    def fetch(self) -> str:
        if self._data is None:
            self._data = self._load()
        return self._data

class ResourceHandler(ResourceInterface):
    def __init__(self, identifier: str, token: Optional[str] = None):
        self.identifier = identifier
        self.token = token
        self._real: Optional[RealResource] = None
        self._cached: Optional[str] = None
        self._allowed_tokens = {"alpha", "beta", "admin"}

    def _authorize(self) -> None:
        if self.token not in self._allowed_tokens:
            raise PermissionError("Access denied: invalid token")

    def _ensure_real(self) -> None:
        if self._real is None:
            self._real = RealResource(self.identifier)

    def fetch(self) -> str:
        try:
            self._authorize()
            if self._cached is None:
                self._ensure_real()
                self._cached = self._real.fetch()
            return self._cached
        except Exception as e:
            raise

    def invalidate_cache(self) -> None:
        self._cached = None

if __name__ == "__main__":
    handler = ResourceHandler("file-123", token="alpha")
    print(handler.fetch())
    print(handler.fetch())
    handler.invalidate_cache()
    print("After invalidation:", handler.fetch())

    try:
        bad_handler = ResourceHandler("file-123", token="guest")
        print(bad_handler.fetch())
    except PermissionError as e:
        print("PermissionError caught:", e)

    try:
        broken = ResourceHandler("", token="admin")
        print(broken.fetch())
    except ValueError as e:
        print("ValueError caught:", e)
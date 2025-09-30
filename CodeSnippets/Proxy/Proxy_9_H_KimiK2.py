import time
from typing import Optional
from functools import wraps

class DatabaseAccessor:
    def fetch(self, key: str) -> str:
        time.sleep(0.5)
        return f"data_for_{key}"

class CachedAccessor:
    def __init__(self, real_accessor: DatabaseAccessor):
        self._real = real_accessor
        self._cache: dict[str, str] = {}
        self._access_count = 0

    def fetch(self, key: str) -> str:
        self._access_count += 1
        if key in self._cache:
            return self._cache[key]
        value = self._real.fetch(key)
        self._cache[key] = value
        return value

    def clear_cache(self) -> None:
        self._cache.clear()

    def get_stats(self) -> dict[str, int]:
        return {"accesses": self._access_count, "cached": len(self._cache)}

class SecureAccessor:
    def __init__(self, real_accessor: CachedAccessor, password: str):
        self._real = real_accessor
        self._password = password
        self._authenticated = False

    def authenticate(self, password: str) -> bool:
        self._authenticated = password == self._password
        return self._authenticated

    def fetch(self, key: str) -> Optional[str]:
        if not self._authenticated:
            return None
        return self._real.fetch(key)

    def clear_cache(self) -> bool:
        if not self._authenticated:
            return False
        self._real.clear_cache()
        return True

    def get_stats(self) -> Optional[dict[str, int]]:
        if not self._authenticated:
            return None
        return self._real.get_stats()

if __name__ == "__main__":
    db = DatabaseAccessor()
    cached = CachedAccessor(db)
    secure = SecureAccessor(cached, "secret123")

    print(secure.fetch("user1"))
    print(secure.authenticate("wrong"))
    print(secure.fetch("user1"))
    print(secure.authenticate("secret123"))
    print(secure.fetch("user1"))
    print(secure.fetch("user2"))
    print(secure.get_stats())
    print(secure.clear_cache())
    print(secure.get_stats())
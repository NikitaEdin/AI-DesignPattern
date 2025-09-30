import time
from abc import ABC, abstractmethod

class DataAccess(ABC):
    @abstractmethod
    def fetch(self) -> str:
        pass

class DataService(DataAccess):
    def fetch(self) -> str:
        time.sleep(2)
        return "Real data from service"

class DataGuard(DataAccess):
    def __init__(self):
        self._real = DataService()
        self._cache = None

    def fetch(self) -> str:
        if self._cache is None:
            try:
                self._cache = self._real.fetch()
            except Exception:
                return "Fallback data"
        return self._cache

if __name__ == "__main__":
    guard = DataGuard()
    print("First call:", guard.fetch())
    print("Second call:", guard.fetch())
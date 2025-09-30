from abc import ABC, abstractmethod
import time
from threading import Lock


class DataService(ABC):
    @abstractmethod
    def fetch_data(self, key: str) -> str:
        pass


class RealDataService(DataService):
    def fetch_data(self, key: str) -> str:
        time.sleep(0.5)
        return f"Data for {key}"


class CachedDataService(DataService):
    def __init__(self):
        self._real_service = RealDataService()
        self._cache = {}
        self._lock = Lock()

    def fetch_data(self, key: str) -> str:
        with self._lock:
            if key in self._cache:
                return self._cache[key]
        
        data = self._real_service.fetch_data(key)
        
        with self._lock:
            self._cache[key] = data
        
        return data


if __name__ == "__main__":
    service = CachedDataService()
    
    for i in range(2):
        start = time.time()
        result = service.fetch_data("item1")
        elapsed = time.time() - start
        print(f"Call {i+1}: {result} ({elapsed:.2f}s)")
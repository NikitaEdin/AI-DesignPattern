import time
from abc import ABC, abstractmethod

class DataService(ABC):
    @abstractmethod
    def fetch(self, key):
        pass

class RealDataService(DataService):
    def fetch(self, key):
        print("Loading heavy data...")
        time.sleep(0.5)
        return f"Data for {key}"

class CachedDataService(DataService):
    def __init__(self):
        self._real_service = RealDataService()
        self._cache = {}

    def fetch(self, key):
        if key in self._cache:
            return self._cache[key]
        data = self._real_service.fetch(key)
        self._cache[key] = data
        return data

def main():
    service = CachedDataService()
    print(service.fetch("user123"))
    print(service.fetch("user123"))

if __name__ == "__main__":
    main()
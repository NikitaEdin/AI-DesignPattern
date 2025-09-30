import time
from abc import ABC, abstractmethod

class DataAccessInterface(ABC):
    @abstractmethod
    def fetch_data(self, key):
        pass

class RealDataReader(DataAccessInterface):
    def fetch_data(self, key):
        time.sleep(2)
        return f"Data for {key}"

class CachedDataReader(DataAccessInterface):
    def __init__(self):
        self._reader = RealDataReader()
        self._cache = {}

    def fetch_data(self, key):
        if key in self._cache:
            print("Cache hit")
            return self._cache[key]
        print("Cache miss")
        data = self._reader.fetch_data(key)
        self._cache[key] = data
        return data

if __name__ == "__main__":
    reader = CachedDataReader()
    print(reader.fetch_data("user1"))
    print(reader.fetch_data("user1"))
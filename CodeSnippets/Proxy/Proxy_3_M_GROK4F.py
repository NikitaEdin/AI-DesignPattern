import time

class DataProvider:
    def __init__(self):
        self._data = {
            "user1": "Detailed profile information for user1",
            "user2": "Detailed profile information for user2"
        }

    def fetch_data(self, key):
        if key not in self._data:
            raise ValueError("Invalid key provided")
        time.sleep(2)  # Simulate expensive operation
        return self._data[key]

class BufferedDataProvider:
    def __init__(self):
        self._provider = DataProvider()
        self._buffer = {}

    def fetch_data(self, key):
        if not key:
            raise ValueError("Key cannot be empty")
        if key not in self._buffer:
            print(f"Fetching data for {key} from source...")
            self._buffer[key] = self._provider.fetch_data(key)
        else:
            print(f"Retrieving data for {key} from buffer")
        return self._buffer[key]

if __name__ == "__main__":
    provider = BufferedDataProvider()
    import time

    start = time.time()
    data1 = provider.fetch_data("user1")
    elapsed1 = time.time() - start
    print(f"First retrieval: {data1[:20]}..., time: {elapsed1:.2f}s\n")

    start = time.time()
    data2 = provider.fetch_data("user1")
    elapsed2 = time.time() - start
    print(f"Second retrieval: {data2[:20]}..., time: {elapsed2:.2f}s")
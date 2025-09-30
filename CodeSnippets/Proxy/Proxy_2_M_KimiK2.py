import time

class NetworkResource:
    def fetch_data(self):
        return "Data from network resource"

class CachedNetworkAccessor:
    def __init__(self, real_resource):
        self._real_resource = real_resource
        self._cache = None
        self._last_update = 0
        self._ttl = 5  # seconds

    def fetch_data(self):
        current_time = time.time()
        if self._cache is None or (current_time - self._last_update) > self._ttl:
            try:
                self._cache = self._real_resource.fetch_data()
                self._last_update = current_time
                print("Cache updated")
            except Exception as e:
                print(f"Failed to fetch fresh data: {e}")
                if self._cache is None:
                    return "No data available"
                print("Returning cached data")
        else:
            print("Returning cached data")
        return self._cache

if __name__ == "__main__":
    real_resource = NetworkResource()
    accessor = CachedNetworkAccessor(real_resource)
    print(accessor.fetch_data())
    print(accessor.fetch_data())
    time.sleep(6)
    print(accessor.fetch_data())
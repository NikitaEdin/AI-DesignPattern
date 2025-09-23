class Service:
    def request(self, data):
        raise NotImplementedError

class RealService(Service):
    def __init__(self):
        self._ready = True
    def request(self, data):
        return f"RealService processed: {data}"

class ServiceWrapper(Service):
    def __init__(self):
        self._real = None
        self._cache = {}
    def request(self, data):
        if data in self._cache:
            return f"Cached: {self._cache[data]}"
        if self._real is None:
            self._real = RealService()
        result = self._real.request(data)
        self._cache[data] = result
        return result

if __name__ == "__main__":
    wrapper = ServiceWrapper()
    print(wrapper.request("task1"))
    print(wrapper.request("task1"))
    print(wrapper.request("task2"))
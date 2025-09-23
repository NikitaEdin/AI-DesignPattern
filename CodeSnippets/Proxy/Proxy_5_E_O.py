class Subject:
    def request(self):
        raise NotImplementedError

class RealService(Subject):
    def __init__(self):
        self.state = "ready"
    def request(self):
        return f"RealService ({self.state}): handling request"

class ServiceWrapper(Subject):
    def __init__(self, real=None):
        self._real = real
    def request(self):
        if self._real is None:
            self._real = RealService()
            return "Wrapper: initialized real service and forwarded -> " + self._real.request()
        return "Wrapper: forwarded -> " + self._real.request()

if __name__ == "__main__":
    wrapper = ServiceWrapper()
    print(wrapper.request())
    print(wrapper.request())
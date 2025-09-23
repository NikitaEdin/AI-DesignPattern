class ServiceInterface:
    def request(self) -> str:
        raise NotImplementedError

class HeavyService(ServiceInterface):
    def __init__(self):
        self._data = "heavy resource initialized"
    def request(self) -> str:
        return f"Real service response with {self._data}"

class ServiceGuard(ServiceInterface):
    def __init__(self):
        self._real = None
    def request(self) -> str:
        if self._real is None:
            self._real = HeavyService()
        return self._real.request()

if __name__ == "__main__":
    guard = ServiceGuard()
    print(guard.request())
    print(guard.request())
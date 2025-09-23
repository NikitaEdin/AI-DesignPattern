from abc import ABC, abstractmethod
class Service(ABC):
    @abstractmethod
    def request(self): pass
class RealService(Service):
    def request(self): return "RealService: request handled"
class ServiceGuard(Service):
    def __init__(self, real, allowed=True):
        self._real = real; self._allowed = allowed
    def request(self):
        return self._real.request() if self._allowed else "ServiceGuard: access denied"
if __name__ == "__main__":
    real = RealService()
    allowed = ServiceGuard(real, allowed=True)
    denied = ServiceGuard(real, allowed=False)
    print(allowed.request())
    print(denied.request())
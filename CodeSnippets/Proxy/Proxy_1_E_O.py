class Service:
    def perform(self):
        raise NotImplementedError

class RealService(Service):
    def perform(self):
        return "RealService: operation completed"

class ServiceGuard(Service):
    def __init__(self, authorized):
        self._authorized = authorized
        self._real = None
    def perform(self):
        if not self._authorized:
            return "Access denied"
        if self._real is None:
            self._real = RealService()
        return self._real.perform()

if __name__ == "__main__":
    allowed = ServiceGuard(True)
    denied = ServiceGuard(False)
    print(allowed.perform())
    print(denied.perform())
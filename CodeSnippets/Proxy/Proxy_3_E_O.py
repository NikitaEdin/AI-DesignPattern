class Service:
    def request(self):
        raise NotImplementedError

class RealService(Service):
    def request(self):
        return "RealService: handled request"

class ServiceHandler(Service):
    def __init__(self, real=None):
        self._real = real
    def request(self):
        if not self._check_access():
            return "Access denied"
        if self._real is None:
            self._real = RealService()
        result = self._real.request()
        self._log_access()
        return result
    def _check_access(self):
        return True
    def _log_access(self):
        pass

if __name__ == "__main__":
    handler = ServiceHandler()
    print(handler.request())
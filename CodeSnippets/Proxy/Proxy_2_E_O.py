class Service:
    def request(self):
        raise NotImplementedError

class RealService(Service):
    def request(self):
        return "Real service: processing request"

class AccessService(Service):
    def __init__(self):
        self._real = None
    def request(self):
        if self._check_access():
            if self._real is None:
                self._real = RealService()
            return self._real.request()
        return "Access denied"
    def _check_access(self):
        return True

if __name__ == "__main__":
    client = AccessService()
    print(client.request())
    direct = RealService()
    print(direct.request())
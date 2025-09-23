class Target:
    def request(self):
        raise NotImplementedError

class OldService:
    def specific_request(self):
        return "Old service result"

class ServiceWrapper(Target):
    def __init__(self, old):
        self.old = old
    def request(self):
        return f"Wrapped: {self.old.specific_request()}"

if __name__ == '__main__':
    old = OldService()
    wrapped = ServiceWrapper(old)
    print(wrapped.request())
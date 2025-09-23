class Service:
    def operation(self):
        raise NotImplementedError

class SimpleService(Service):
    def operation(self):
        return "hello"

class ServiceWrapper(Service):
    def __init__(self, service):
        self._service = service
    def operation(self):
        return self._service.operation()

class UppercaseWrapper(ServiceWrapper):
    def operation(self):
        return self._service.operation().upper()

class BracketsWrapper(ServiceWrapper):
    def operation(self):
        return "[" + self._service.operation() + "]"

if __name__ == "__main__":
    s = SimpleService()
    print(s.operation())
    wrapped = UppercaseWrapper(BracketsWrapper(s))
    print(wrapped.operation())
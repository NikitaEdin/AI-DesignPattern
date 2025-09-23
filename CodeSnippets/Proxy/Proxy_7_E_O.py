class ServiceInterface:
    def perform(self):
        raise NotImplementedError

class RealService(ServiceInterface):
    def perform(self):
        return "Real service result"

class ServiceWrapper(ServiceInterface):
    def __init__(self):
        self._real = None
    def perform(self):
        if not self._real:
            self._real = RealService()
        return f"Wrapped -> {self._real.perform()}"

if __name__ == "__main__":
    wrapper = ServiceWrapper()
    print(wrapper.perform())
    print(wrapper.perform())
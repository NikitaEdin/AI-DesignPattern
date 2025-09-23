class System:
    def __init__(self):
        self._component1 = None
        self._component2 = None

    @property
    def component1(self):
        return self._component1

    @property
    def component2(self):
        return self._component2

class Facade:
    def __init__(self, system):
        self._system = system

    def operation1(self):
        self._system.component1.operation1()

    def operation2(self):
        self._system.component2.operation2()

if __name__ == "__main__":
    system = System()
    facade = Facade(system)
    facade.operation1()
    facade.operation2()
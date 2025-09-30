class Subject:
    def __init__(self):
        self._dependents = []

    def attach(self, dependent):
        self._dependents.append(dependent)

    def notify(self):
        for dependent in self._dependents:
            dependent.update(self)

class Data(Subject):
    def __init__(self):
        super().__init__()
        self._value = None

    def set_value(self, value):
        self._value = value
        self.notify()

    def get_value(self):
        return self._value

class Dependent:
    def update(self, subject):
        pass

class ConcreteDependent(Dependent):
    def update(self, subject):
        print("New value:", subject.get_value())

if __name__ == "__main__":
    data = Data()
    dep = ConcreteDependent()
    data.attach(dep)
    data.set_value(10)
python
class Facade:
    def __init__(self, subsystem1, subsystem2):
        self.subsystem1 = subsystem1
        self.subsystem2 = subsystem2

    def method(self):
        self.subsystem1.operation1()
        self.subsystem2.operation2()

class Subsystem1:
    def operation1(self):
        print("Subsystem1")

class Subsystem2:
    def operation2(self):
        print("Subsystem2")

if __name__ == "__main__":
    facade = Facade(Subsystem1(), Subsystem2())
    facade.method()
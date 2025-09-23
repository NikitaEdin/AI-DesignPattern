class Facade:
    def __init__(self, subsystem1, subsystem2):
        self.subsystem1 = subsystem1
        self.subsystem2 = subsystem2

    def method(self):
        self.subsystem1.method()
        self.subsystem2.method()

class Subsystem1:
    def method(self):
        print("Subsystem 1")

class Subsystem2:
    def method(self):
        print("Subsystem 2")

if __name__ == "__main__":
    facade = Facade(Subsystem1(), Subsystem2())
    facade.method()
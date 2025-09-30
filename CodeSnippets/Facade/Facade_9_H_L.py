class Facade:
    def __init__(self, subsystem1, subsystem2):
        self.subsystem1 = subsystem1
        self.subsystem2 = subsystem2

    def method(self):
        # perform some operation on the subsystems
        result = self.subsystem1.operation1() + self.subsystem2.operation2()
        return result
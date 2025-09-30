import abc

class Mode(abc.ABC):
    @abc.abstractmethod
    def perform(self, data):
        pass

class Addition(Mode):
    def perform(self, data):
        return sum(data)

class Multiplication(Mode):
    def perform(self, data):
        prod = 1
        for n in data:
            prod *= n
        return prod

class Processor:
    def __init__(self):
        self.mode = None
    def set_mode(self, mode: Mode):
        self.mode = mode
    def execute(self, data):
        return self.mode.perform(data)

if __name__ == "__main__":
    p = Processor()
    p.set_mode(Addition())
    print(p.execute([1, 2, 3]))
    p.set_mode(Multiplication())
    print(p.execute([1, 2, 3]))
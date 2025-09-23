from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class MultiplyOperation(Operation):
    def execute(self, a, b):
        return a * b

class Calculator:
    def __init__(self, op):
        self.op = op

    def compute(self, a, b):
        return self.op.execute(a, b)

if __name__ == "__main__":
    calc1 = Calculator(AddOperation())
    print(calc1.compute(5, 3))
    calc2 = Calculator(MultiplyOperation())
    print(calc2.compute(5, 3))
from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def calculate(self, a, b):
        pass

class Adder(Operation):
    def calculate(self, a, b):
        return a + b

class Subtractor(Operation):
    def calculate(self, a, b):
        return a - b

class Calculator:
    def __init__(self, op):
        self.op = op

    def set_operation(self, op):
        self.op = op

    def compute(self, a, b):
        return self.op.calculate(a, b)

if __name__ == "__main__":
    calc = Calculator(Adder())
    print(calc.compute(5, 3))
    calc.set_operation(Subtractor())
    print(calc.compute(5, 3))
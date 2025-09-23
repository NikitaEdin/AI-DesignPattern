from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class SubtractOperation(Operation):
    def execute(self, a, b):
        return a - b

class Calculator:
    def __init__(self, op):
        self.op = op

    def set_operation(self, op):
        self.op = op

    def calculate(self, a, b):
        return self.op.execute(a, b)

if __name__ == "__main__":
    calc = Calculator(AddOperation())
    print(calc.calculate(5, 3))
    calc.set_operation(SubtractOperation())
    print(calc.calculate(5, 3))
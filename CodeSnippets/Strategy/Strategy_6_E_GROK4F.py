from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def compute(self, a, b):
        pass

class Addition(Operation):
    def compute(self, a, b):
        return a + b

class Subtraction(Operation):
    def compute(self, a, b):
        return a - b

class Calculator:
    def __init__(self, operation):
        self.operation = operation

    def set_operation(self, operation):
        self.operation = operation

    def calculate(self, a, b):
        return self.operation.compute(a, b)

if __name__ == "__main__":
    calc = Calculator(Addition())
    print(calc.calculate(5, 3))  # Output: 8
    calc.set_operation(Subtraction())
    print(calc.calculate(5, 3))  # Output: 2
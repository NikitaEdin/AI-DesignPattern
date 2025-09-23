from abc import ABC, abstractmethod
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b): pass
class Add(Operation):
    def execute(self, a, b): return a + b
class Multiply(Operation):
    def execute(self, a, b): return a * b
class Calculator:
    def __init__(self, operation: Operation = None): self.operation = operation
    def set_operation(self, operation: Operation): self.operation = operation
    def calculate(self, a, b):
        if not self.operation: raise ValueError("No operation set")
        return self.operation.execute(a, b)
if __name__ == "__main__":
    calc = Calculator()
    calc.set_operation(Add())
    print(calc.calculate(2, 3))
    calc.set_operation(Multiply())
    print(calc.calculate(2, 3))
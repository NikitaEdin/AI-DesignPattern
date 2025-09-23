class Operation:
    def execute(self, a, b): raise NotImplementedError

class AddOperation(Operation):
    def execute(self, a, b): return a + b

class MultiplyOperation(Operation):
    def execute(self, a, b): return a * b

class Calculator:
    def __init__(self, operation): self.operation = operation
    def set_operation(self, operation): self.operation = operation
    def calculate(self, a, b): return self.operation.execute(a, b)

if __name__ == "__main__":
    add = AddOperation()
    mul = MultiplyOperation()
    calc = Calculator(add)
    print(calc.calculate(2, 3))
    calc.set_operation(mul)
    print(calc.calculate(2, 3))
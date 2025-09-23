class Operation:
    def execute(self, a, b):
        raise NotImplementedError

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Calculator:
    def __init__(self, operation):
        self.operation = operation
    def set_operation(self, operation):
        self.operation = operation
    def calculate(self, a, b):
        return self.operation.execute(a, b)

if __name__ == "__main__":
    calc = Calculator(Add())
    print(calc.calculate(3, 4))
    calc.set_operation(Multiply())
    print(calc.calculate(3, 4))
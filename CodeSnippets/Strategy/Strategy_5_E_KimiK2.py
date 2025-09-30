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
        
    def compute(self, a, b):
        return self.operation.execute(a, b)

if __name__ == "__main__":
    calc = Calculator(Add())
    print(calc.compute(3, 4))
    calc.operation = Multiply()
    print(calc.compute(3, 4))
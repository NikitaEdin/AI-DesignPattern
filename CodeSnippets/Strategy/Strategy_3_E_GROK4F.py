class Operation:
    def execute(self, a, b):
        pass

class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class SubtractOperation(Operation):
    def execute(self, a, b):
        return a - b

class Calculator:
    def __init__(self):
        self.operation = None

    def set_operation(self, op):
        self.operation = op

    def calculate(self, a, b):
        if self.operation:
            return self.operation.execute(a, b)
        return None

if __name__ == "__main__":
    calc = Calculator()
    calc.set_operation(AddOperation())
    print(calc.calculate(5, 3))
    calc.set_operation(SubtractOperation())
    print(calc.calculate(5, 3))
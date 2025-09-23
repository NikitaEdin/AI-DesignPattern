class Operation:
    def do(self, a, b):
        raise NotImplementedError

class AddOperation(Operation):
    def do(self, a, b):
        return a + b

class MultiplyOperation(Operation):
    def do(self, a, b):
        return a * b

class Calculator:
    def __init__(self, algorithm: Operation):
        self.algorithm = algorithm
    def set_algorithm(self, algorithm: Operation):
        self.algorithm = algorithm
    def execute(self, a, b):
        return self.algorithm.do(a, b)

if __name__ == "__main__":
    calc = Calculator(AddOperation())
    print(calc.execute(3, 4))
    calc.set_algorithm(MultiplyOperation())
    print(calc.execute(3, 4))
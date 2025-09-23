class Calculator:
    def __init__(self, operation):
        self.operation = operation
    
    def calculate(self, a, b):
        return self.operation.execute(a, b)

class Addition:
    def execute(self, a, b):
        return a + b

class Subtraction:
    def execute(self, a, b):
        return a - b

class Multiplication:
    def execute(self, a, b):
        return a * b

if __name__ == "__main__":
    calc = Calculator(Addition())
    print(calc.calculate(5, 3))
    
    calc = Calculator(Subtraction())
    print(calc.calculate(5, 3))
    
    calc = Calculator(Multiplication())
    print(calc.calculate(5, 3))
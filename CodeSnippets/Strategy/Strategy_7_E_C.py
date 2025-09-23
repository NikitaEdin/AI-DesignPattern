class Calculator:
    def __init__(self, operation):
        self.operation = operation
    
    def execute(self, a, b):
        return self.operation.calculate(a, b)

class Addition:
    def calculate(self, a, b):
        return a + b

class Subtraction:
    def calculate(self, a, b):
        return a - b

class Multiplication:
    def calculate(self, a, b):
        return a * b

if __name__ == "__main__":
    calc = Calculator(Addition())
    print(calc.execute(5, 3))
    
    calc = Calculator(Subtraction())
    print(calc.execute(5, 3))
    
    calc = Calculator(Multiplication())
    print(calc.execute(5, 3))
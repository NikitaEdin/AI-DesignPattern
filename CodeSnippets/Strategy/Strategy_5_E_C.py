class Addition:
    def calculate(self, a, b):
        return a + b

class Multiplication:
    def calculate(self, a, b):
        return a * b

class Calculator:
    def __init__(self, operation):
        self.operation = operation
    
    def set_operation(self, operation):
        self.operation = operation
    
    def execute(self, a, b):
        return self.operation.calculate(a, b)

if __name__ == "__main__":
    add = Addition()
    multiply = Multiplication()
    
    calc = Calculator(add)
    print(calc.execute(5, 3))
    
    calc.set_operation(multiply)
    print(calc.execute(5, 3))
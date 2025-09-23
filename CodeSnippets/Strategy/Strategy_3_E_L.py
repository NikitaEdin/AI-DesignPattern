class Calculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def calculate(self, x, y):
        return self.strategy.calculate(x, y)

class AdditionStrategy:
    def calculate(self, x, y):
        return x + y

class SubtractionStrategy:
    def calculate(self, x, y):
        return x - y

# Usage example

calculator = Calculator(AdditionStrategy())
result = calculator.calculate(2, 3) # Output: 5

calculator = Calculator(SubtractionStrategy())
result = calculator.calculate(2, 3) # Output: -1
import math

# Strategy Interface
class AreaStrategy:
    def calculate(self, dimension):
        raise NotImplementedError

# Concrete Strategy
class CircleAreaStrategy(AreaStrategy):
    def calculate(self, radius):
        # Only one algorithm is ever implemented
        if radius <= 0:
            return 0.0
        return math.pi * radius**2

# Context
class AreaCalculator:
    def __init__(self, strategy):
        # Context is initialized with a fixed strategy
        self._strategy = strategy

    def execute_calculation(self, dimension):
        # The Context just delegates the fixed calculation
        return self._strategy.calculate(dimension)

# Example Usage
r = 5.0
circle_strategy = CircleAreaStrategy()
calculator = AreaCalculator(circle_strategy)
area = calculator.execute_calculation(r)
print(f"The area for radius {r} is {area:.2f}")
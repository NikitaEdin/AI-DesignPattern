from abc import ABC, abstractmethod
from typing import Optional, Union

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Addition(Operation):
    def execute(self, a: float, b: float) -> float:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Inputs must be numeric")
        return a + b

class Subtraction(Operation):
    def execute(self, a: float, b: float) -> float:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Inputs must be numeric")
        return a - b

class Multiplication(Operation):
    def execute(self, a: float, b: float) -> float:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Inputs must be numeric")
        return a * b

class Division(Operation):
    def execute(self, a: float, b: float) -> float:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Inputs must be numeric")
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

class SimpleCalculator:
    def __init__(self, operation: Optional[Operation] = None):
        if operation is not None and not isinstance(operation, Operation):
            raise ValueError("Provided operation must implement Operation")
        self._current_operation: Optional[Operation] = operation

    def set_operation(self, operation: Operation) -> None:
        if not isinstance(operation, Operation):
            raise ValueError("Operation must implement Operation")
        self._current_operation = operation

    def calculate(self, a: float, b: float) -> float:
        if self._current_operation is None:
            raise ValueError("No operation is set")
        return self._current_operation.execute(a, b)

def main():
    calc = SimpleCalculator()
    
    add_op = Addition()
    calc.set_operation(add_op)
    print(f"5 + 3 = {calc.calculate(5, 3)}")
    
    sub_op = Subtraction()
    calc.set_operation(sub_op)
    print(f"5 - 3 = {calc.calculate(5, 3)}")
    
    mul_op = Multiplication()
    calc.set_operation(mul_op)
    print(f"5 * 3 = {calc.calculate(5, 3)}")
    
    div_op = Division()
    calc.set_operation(div_op)
    print(f"6 / 2 = {calc.calculate(6, 2)}")
    
    try:
        print(f"5 / 0 = {calc.calculate(5, 0)}")
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        print(f"'a' + 3 = {calc.set_operation(add_op) and calc.calculate('a', 3)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
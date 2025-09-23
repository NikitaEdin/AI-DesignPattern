from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddOperation(Operation):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        self.calculator.result += self.value

    def undo(self):
        self.calculator.result -= self.value

class SubtractOperation(Operation):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        self.calculator.result -= self.value

    def undo(self):
        self.calculator.result += self.value

class SimpleCalculator:
    def __init__(self):
        self.result = 0

class CalculatorController:
    def __init__(self, calculator):
        self.calculator = calculator
        self.history = []

    def perform(self, operation):
        try:
            operation.execute()
            self.history.append(operation)
        except Exception as e:
            print(f"Execution failed: {e}")

    def undo_last(self):
        if self.history:
            last_operation = self.history.pop()
            last_operation.undo()
        else:
            print("No operations to undo")

if __name__ == "__main__":
    calc = SimpleCalculator()
    controller = CalculatorController(calc)

    add_op = AddOperation(calc, 10)
    controller.perform(add_op)
    print(f"After add: {calc.result}")

    subtract_op = SubtractOperation(calc, 4)
    controller.perform(subtract_op)
    print(f"After subtract: {calc.result}")

    controller.undo_last()
    print(f"After undo: {calc.result}")
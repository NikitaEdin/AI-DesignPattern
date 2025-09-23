from abc import ABC, abstractmethod
from typing import List, Any
import time

class Action(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        pass

class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, amount: float) -> float:
        self.value += amount
        return self.value
    
    def subtract(self, amount: float) -> float:
        self.value -= amount
        return self.value
    
    def multiply(self, factor: float) -> float:
        self.value *= factor
        return self.value

class AddOperation(Action):
    def __init__(self, calculator: Calculator, amount: float):
        self.calculator = calculator
        self.amount = amount
        self.executed = False
    
    def execute(self) -> float:
        result = self.calculator.add(self.amount)
        self.executed = True
        return result
    
    def undo(self) -> float:
        if self.executed:
            result = self.calculator.subtract(self.amount)
            self.executed = False
            return result
        return self.calculator.value
    
    def can_undo(self) -> bool:
        return self.executed

class MultiplyOperation(Action):
    def __init__(self, calculator: Calculator, factor: float):
        self.calculator = calculator
        self.factor = factor
        self.previous_value = None
        self.executed = False
    
    def execute(self) -> float:
        self.previous_value = self.calculator.value
        result = self.calculator.multiply(self.factor)
        self.executed = True
        return result
    
    def undo(self) -> float:
        if self.executed and self.previous_value is not None:
            self.calculator.value = self.previous_value
            self.executed = False
            return self.calculator.value
        return self.calculator.value
    
    def can_undo(self) -> bool:
        return self.executed and self.previous_value is not None

class MacroOperation(Action):
    def __init__(self, operations: List[Action]):
        self.operations = operations
        self.executed_operations: List[Action] = []
    
    def execute(self) -> List[Any]:
        results = []
        self.executed_operations.clear()
        for operation in self.operations:
            try:
                result = operation.execute()
                results.append(result)
                self.executed_operations.append(operation)
            except Exception:
                self.undo()
                raise
        return results
    
    def undo(self) -> List[Any]:
        results = []
        for operation in reversed(self.executed_operations):
            if operation.can_undo():
                results.append(operation.undo())
        self.executed_operations.clear()
        return results
    
    def can_undo(self) -> bool:
        return len(self.executed_operations) > 0

class Invoker:
    def __init__(self):
        self.history: List[Action] = []
        self.current_position = -1
    
    def execute_action(self, action: Action) -> Any:
        result = action.execute()
        if self.current_position < len(self.history) - 1:
            self.history = self.history[:self.current_position + 1]
        self.history.append(action)
        self.current_position += 1
        return result
    
    def undo_last(self) -> Any:
        if self.current_position >= 0:
            action = self.history[self.current_position]
            if action.can_undo():
                result = action.undo()
                self.current_position -= 1
                return result
        return None
    
    def redo_next(self) -> Any:
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            action = self.history[self.current_position]
            return action.execute()
        return None

if __name__ == "__main__":
    calc = Calculator()
    invoker = Invoker()
    
    add_five = AddOperation(calc, 5)
    multiply_three = MultiplyOperation(calc, 3)
    add_ten = AddOperation(calc, 10)
    
    print(f"Initial: {calc.value}")
    
    invoker.execute_action(add_five)
    print(f"After +5: {calc.value}")
    
    invoker.execute_action(multiply_three)
    print(f"After *3: {calc.value}")
    
    macro = MacroOperation([AddOperation(calc, 2), MultiplyOperation(calc, 2)])
    invoker.execute_action(macro)
    print(f"After macro (+2, *2): {calc.value}")
    
    invoker.undo_last()
    print(f"After undo macro: {calc.value}")
    
    invoker.undo_last()
    print(f"After undo multiply: {calc.value}")
    
    invoker.redo_next()
    print(f"After redo: {calc.value}")
from abc import ABC, abstractmethod
from typing import List, Any
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor

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

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.executed_actions = []
    
    def execute(self) -> List[Any]:
        results = []
        for action in self.actions:
            try:
                result = action.execute()
                self.executed_actions.append(action)
                results.append(result)
            except Exception as e:
                self.undo()
                raise e
        return results
    
    def undo(self) -> List[Any]:
        results = []
        for action in reversed(self.executed_actions):
            if action.can_undo():
                results.append(action.undo())
        self.executed_actions.clear()
        return results
    
    def can_undo(self) -> bool:
        return len(self.executed_actions) > 0

class Calculator:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()
    
    def add(self, amount: float) -> float:
        with self._lock:
            self.value += amount
            return self.value
    
    def subtract(self, amount: float) -> float:
        with self._lock:
            self.value -= amount
            return self.value

class MathOperation(Action):
    def __init__(self, calculator: Calculator, operation: str, amount: float):
        self.calculator = calculator
        self.operation = operation
        self.amount = amount
        self.executed = False
    
    def execute(self) -> float:
        if self.operation == "add":
            result = self.calculator.add(self.amount)
        elif self.operation == "subtract":
            result = self.calculator.subtract(self.amount)
        else:
            raise ValueError(f"Unknown operation: {self.operation}")
        self.executed = True
        return result
    
    def undo(self) -> float:
        if not self.can_undo():
            raise RuntimeError("Cannot undo operation")
        
        if self.operation == "add":
            result = self.calculator.subtract(self.amount)
        else:
            result = self.calculator.add(self.amount)
        
        self.executed = False
        return result
    
    def can_undo(self) -> bool:
        return self.executed

class Processor:
    def __init__(self):
        self.history = []
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def execute(self, action: Action) -> Any:
        result = action.execute()
        self.history.append(action)
        return result
    
    def execute_async(self, action: Action):
        return self.executor.submit(self.execute, action)
    
    def undo_last(self) -> Any:
        if not self.history:
            raise RuntimeError("No actions to undo")
        
        last_action = self.history[-1]
        if not last_action.can_undo():
            raise RuntimeError("Last action cannot be undone")
        
        result = last_action.undo()
        self.history.pop()
        return result
    
    def save_state(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self.history, f)
    
    def load_state(self, filename: str):
        with open(filename, 'rb') as f:
            self.history = pickle.load(f)

if __name__ == "__main__":
    calc = Calculator()
    processor = Processor()
    
    add_op = MathOperation(calc, "add", 10)
    sub_op = MathOperation(calc, "subtract", 5)
    add_op2 = MathOperation(calc, "add", 3)
    
    print(f"Initial value: {calc.value}")
    
    result1 = processor.execute(add_op)
    print(f"After adding 10: {result1}")
    
    macro = MacroAction([sub_op, add_op2])
    result2 = processor.execute(macro)
    print(f"After macro (subtract 5, add 3): {calc.value}")
    
    processor.undo_last()
    print(f"After undoing macro: {calc.value}")
    
    processor.undo_last()
    print(f"After undoing add 10: {calc.value}")
    
    future = processor.execute_async(MathOperation(calc, "add", 20))
    result3 = future.result()
    print(f"Async add 20: {result3}")
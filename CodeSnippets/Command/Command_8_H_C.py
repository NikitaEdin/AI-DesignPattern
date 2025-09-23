from abc import ABC, abstractmethod
from typing import List, Optional
import threading
from functools import wraps
from enum import Enum

class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3

class Action(ABC):
    def __init__(self, priority: Priority = Priority.NORMAL):
        self.priority = priority
        self.timestamp = None
        self._executed = False
        
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass
    
    @property
    def executed(self) -> bool:
        return self._executed

def thread_safe(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)
    return wrapper

class Orchestrator:
    def __init__(self, max_history: int = 100):
        self._history: List[Action] = []
        self._queue: List[Action] = []
        self._max_history = max_history
        self._lock = threading.RLock()
    
    @thread_safe
    def schedule(self, action: Action) -> None:
        self._queue.append(action)
        self._queue.sort(key=lambda x: (-x.priority.value, id(x)))
    
    @thread_safe
    def execute_next(self) -> Optional[Action]:
        if not self._queue:
            return None
        
        action = self._queue.pop(0)
        if action.execute():
            action._executed = True
            self._add_to_history(action)
            return action
        return None
    
    @thread_safe
    def execute_all(self) -> List[Action]:
        executed = []
        while self._queue:
            action = self.execute_next()
            if action:
                executed.append(action)
            else:
                break
        return executed
    
    @thread_safe
    def undo_last(self) -> bool:
        if not self._history:
            return False
        
        action = self._history.pop()
        if action.undo():
            action._executed = False
            return True
        
        self._history.append(action)
        return False
    
    def _add_to_history(self, action: Action) -> None:
        self._history.append(action)
        if len(self._history) > self._max_history:
            self._history.pop(0)
    
    @property
    def pending_count(self) -> int:
        return len(self._queue)
    
    @property
    def history_count(self) -> int:
        return len(self._history)

class FileOperation(Action):
    def __init__(self, filename: str, content: str, priority: Priority = Priority.NORMAL):
        super().__init__(priority)
        self.filename = filename
        self.content = content
        self._backup_content = None
    
    def execute(self) -> bool:
        try:
            try:
                with open(self.filename, 'r') as f:
                    self._backup_content = f.read()
            except FileNotFoundError:
                self._backup_content = None
            
            with open(self.filename, 'w') as f:
                f.write(self.content)
            return True
        except Exception:
            return False
    
    def undo(self) -> bool:
        try:
            if self._backup_content is None:
                import os
                if os.path.exists(self.filename):
                    os.remove(self.filename)
            else:
                with open(self.filename, 'w') as f:
                    f.write(self._backup_content)
            return True
        except Exception:
            return False

class Calculator:
    def __init__(self):
        self.value = 0

class MathOperation(Action):
    def __init__(self, calculator: Calculator, operation: str, operand: float, priority: Priority = Priority.NORMAL):
        super().__init__(priority)
        self.calculator = calculator
        self.operation = operation
        self.operand = operand
        self._previous_value = None
    
    def execute(self) -> bool:
        self._previous_value = self.calculator.value
        
        if self.operation == 'add':
            self.calculator.value += self.operand
        elif self.operation == 'subtract':
            self.calculator.value -= self.operand
        elif self.operation == 'multiply':
            self.calculator.value *= self.operand
        elif self.operation == 'divide' and self.operand != 0:
            self.calculator.value /= self.operand
        else:
            return False
        
        return True
    
    def undo(self) -> bool:
        if self._previous_value is not None:
            self.calculator.value = self._previous_value
            return True
        return False

if __name__ == "__main__":
    orchestrator = Orchestrator(max_history=5)
    calculator = Calculator()
    
    orchestrator.schedule(MathOperation(calculator, 'add', 10, Priority.HIGH))
    orchestrator.schedule(FileOperation('test.txt', 'Hello World', Priority.LOW))
    orchestrator.schedule(MathOperation(calculator, 'multiply', 2, Priority.NORMAL))
    
    print(f"Pending operations: {orchestrator.pending_count}")
    
    executed = orchestrator.execute_all()
    print(f"Executed {len(executed)} operations")
    print(f"Calculator value: {calculator.value}")
    
    orchestrator.undo_last()
    print(f"After undo - Calculator value: {calculator.value}")
    
    print(f"History count: {orchestrator.history_count}")
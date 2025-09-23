from abc import ABC, abstractmethod
from typing import List, Any
import threading
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

class FileOperation(Action):
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content
        self.previous_content = None
        self._executed = False
    
    def execute(self) -> str:
        try:
            with open(self.filename, 'r') as f:
                self.previous_content = f.read()
        except FileNotFoundError:
            self.previous_content = None
        
        with open(self.filename, 'w') as f:
            f.write(self.content)
        self._executed = True
        return f"Written to {self.filename}"
    
    def undo(self) -> str:
        if not self.can_undo():
            raise RuntimeError("Cannot undo this operation")
        
        if self.previous_content is None:
            import os
            os.remove(self.filename)
            result = f"Deleted {self.filename}"
        else:
            with open(self.filename, 'w') as f:
                f.write(self.previous_content)
            result = f"Restored {self.filename}"
        
        self._executed = False
        return result
    
    def can_undo(self) -> bool:
        return self._executed

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.executed_actions = []
    
    def execute(self) -> List[Any]:
        results = []
        self.executed_actions = []
        
        for action in self.actions:
            try:
                result = action.execute()
                results.append(result)
                self.executed_actions.append(action)
            except Exception as e:
                for executed in reversed(self.executed_actions):
                    if executed.can_undo():
                        executed.undo()
                raise e
        
        return results
    
    def undo(self) -> List[Any]:
        if not self.can_undo():
            raise RuntimeError("Cannot undo macro")
        
        results = []
        for action in reversed(self.executed_actions):
            if action.can_undo():
                results.append(action.undo())
        
        self.executed_actions = []
        return results
    
    def can_undo(self) -> bool:
        return len(self.executed_actions) > 0

class Scheduler:
    def __init__(self):
        self.history: List[Action] = []
        self.undo_stack: List[Action] = []
        self._lock = threading.Lock()
    
    def execute(self, action: Action) -> Any:
        with self._lock:
            result = action.execute()
            self.history.append(action)
            self.undo_stack.clear()
            return result
    
    def undo_last(self) -> Any:
        with self._lock:
            if not self.history:
                raise RuntimeError("No operations to undo")
            
            last_action = self.history.pop()
            if not last_action.can_undo():
                raise RuntimeError("Last operation cannot be undone")
            
            result = last_action.undo()
            self.undo_stack.append(last_action)
            return result
    
    def redo_last(self) -> Any:
        with self._lock:
            if not self.undo_stack:
                raise RuntimeError("No operations to redo")
            
            action = self.undo_stack.pop()
            result = action.execute()
            self.history.append(action)
            return result
    
    def execute_async(self, action: Action, delay: float = 0):
        def delayed_execute():
            if delay > 0:
                time.sleep(delay)
            self.execute(action)
        
        thread = threading.Thread(target=delayed_execute)
        thread.start()
        return thread

if __name__ == "__main__":
    scheduler = Scheduler()
    
    op1 = FileOperation("test1.txt", "Hello World")
    op2 = FileOperation("test2.txt", "Python Code")
    
    print("Executing single operation:")
    print(scheduler.execute(op1))
    
    print("\nExecuting macro operation:")
    macro = MacroAction([op1, op2])
    print(scheduler.execute(macro))
    
    print("\nUndo last operation:")
    print(scheduler.undo_last())
    
    print("\nRedo last operation:")
    print(scheduler.redo_last())
    
    print("\nAsync execution:")
    thread = scheduler.execute_async(FileOperation("async.txt", "Async content"), 0.1)
    thread.join()
    
    import os
    for f in ["test1.txt", "test2.txt", "async.txt"]:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass
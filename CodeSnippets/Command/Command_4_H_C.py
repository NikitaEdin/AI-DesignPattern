from abc import ABC, abstractmethod
from typing import List, Optional
import threading
import time

class Action(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        pass

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        self.actions = actions
    
    def execute(self) -> None:
        for action in self.actions:
            action.execute()
    
    def undo(self) -> None:
        for action in reversed(self.actions):
            if action.can_undo():
                action.undo()
    
    def can_undo(self) -> bool:
        return all(action.can_undo() for action in self.actions)

class FileOperation(Action):
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content
        self.original_content = None
        self.existed = False
    
    def execute(self) -> None:
        try:
            with open(self.filename, 'r') as f:
                self.original_content = f.read()
                self.existed = True
        except FileNotFoundError:
            self.existed = False
        
        with open(self.filename, 'w') as f:
            f.write(self.content)
    
    def undo(self) -> None:
        if self.existed and self.original_content is not None:
            with open(self.filename, 'w') as f:
                f.write(self.original_content)
        elif not self.existed:
            import os
            os.remove(self.filename)
    
    def can_undo(self) -> bool:
        return True

class AsyncActionExecutor:
    def __init__(self):
        self.history: List[Action] = []
        self.redo_stack: List[Action] = []
    
    def execute(self, action: Action) -> None:
        def run_action():
            action.execute()
            self.history.append(action)
            self.redo_stack.clear()
        
        threading.Thread(target=run_action, daemon=True).start()
    
    def undo(self) -> bool:
        if not self.history:
            return False
        
        action = self.history.pop()
        if action.can_undo():
            action.undo()
            self.redo_stack.append(action)
            return True
        return False
    
    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        
        action = self.redo_stack.pop()
        action.execute()
        self.history.append(action)
        return True

if __name__ == "__main__":
    executor = AsyncActionExecutor()
    
    file_op1 = FileOperation("test1.txt", "Hello World")
    file_op2 = FileOperation("test2.txt", "Python Code")
    
    macro = MacroAction([file_op1, file_op2])
    
    executor.execute(macro)
    time.sleep(0.1)
    
    print("Files created")
    
    if executor.undo():
        print("Macro undone")
    
    if executor.redo():
        print("Macro redone")
    
    import os
    try:
        os.remove("test1.txt")
        os.remove("test2.txt")
    except FileNotFoundError:
        pass
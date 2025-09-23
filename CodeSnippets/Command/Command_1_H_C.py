from abc import ABC, abstractmethod
from typing import List, Any
import json
import time

class Action(ABC):
    def __init__(self):
        self.timestamp = time.time()
        self.metadata = {}
    
    @abstractmethod
    def execute(self) -> Any:
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        pass

class TextEditor:
    def __init__(self):
        self.content = ""
    
    def insert(self, text: str, position: int = None):
        if position is None:
            position = len(self.content)
        self.content = self.content[:position] + text + self.content[position:]
    
    def delete(self, start: int, end: int):
        deleted = self.content[start:end]
        self.content = self.content[:start] + self.content[end:]
        return deleted

class InsertOperation(Action):
    def __init__(self, editor: TextEditor, text: str, position: int = None):
        super().__init__()
        self.editor = editor
        self.text = text
        self.position = position if position is not None else len(editor.content)
        self.executed = False
    
    def execute(self):
        self.editor.insert(self.text, self.position)
        self.executed = True
        return f"Inserted '{self.text}' at position {self.position}"
    
    def undo(self):
        if self.executed:
            self.editor.delete(self.position, self.position + len(self.text))
            self.executed = False
            return f"Undid insert of '{self.text}'"
        return "Nothing to undo"
    
    def can_undo(self) -> bool:
        return self.executed

class DeleteOperation(Action):
    def __init__(self, editor: TextEditor, start: int, end: int):
        super().__init__()
        self.editor = editor
        self.start = start
        self.end = end
        self.deleted_text = ""
        self.executed = False
    
    def execute(self):
        self.deleted_text = self.editor.delete(self.start, self.end)
        self.executed = True
        return f"Deleted '{self.deleted_text}'"
    
    def undo(self):
        if self.executed and self.deleted_text:
            self.editor.insert(self.deleted_text, self.start)
            self.executed = False
            return f"Restored '{self.deleted_text}'"
        return "Nothing to undo"
    
    def can_undo(self) -> bool:
        return self.executed and bool(self.deleted_text)

class MacroOperation(Action):
    def __init__(self, operations: List[Action]):
        super().__init__()
        self.operations = operations
        self.executed_count = 0
    
    def execute(self):
        results = []
        for op in self.operations[self.executed_count:]:
            results.append(op.execute())
            self.executed_count += 1
        return f"Executed macro with {len(results)} operations"
    
    def undo(self):
        results = []
        while self.executed_count > 0:
            op = self.operations[self.executed_count - 1]
            if op.can_undo():
                results.append(op.undo())
            self.executed_count -= 1
        return f"Undid macro ({len(results)} operations)"
    
    def can_undo(self) -> bool:
        return self.executed_count > 0

class ActionManager:
    def __init__(self, max_history: int = 50):
        self.history: List[Action] = []
        self.max_history = max_history
        self.current_position = -1
    
    def execute(self, action: Action):
        result = action.execute()
        self.history = self.history[:self.current_position + 1]
        self.history.append(action)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_position += 1
        return result
    
    def undo(self):
        if self.current_position >= 0:
            action = self.history[self.current_position]
            if action.can_undo():
                result = action.undo()
                self.current_position -= 1
                return result
        return "Nothing to undo"
    
    def redo(self):
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            action = self.history[self.current_position]
            return action.execute()
        return "Nothing to redo"

if __name__ == "__main__":
    editor = TextEditor()
    manager = ActionManager()
    
    print(f"Initial content: '{editor.content}'")
    
    insert1 = InsertOperation(editor, "Hello", 0)
    print(manager.execute(insert1))
    print(f"Content: '{editor.content}'")
    
    insert2 = InsertOperation(editor, " World", 5)
    print(manager.execute(insert2))
    print(f"Content: '{editor.content}'")
    
    delete_op = DeleteOperation(editor, 5, 11)
    macro = MacroOperation([delete_op, InsertOperation(editor, " Python!", 5)])
    print(manager.execute(macro))
    print(f"Content: '{editor.content}'")
    
    print(manager.undo())
    print(f"After undo: '{editor.content}'")
    
    print(manager.redo())
    print(f"After redo: '{editor.content}'")
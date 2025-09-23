from abc import ABC, abstractmethod
from typing import List, Any, Dict
import json
from datetime import datetime

class Action(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        pass
    
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        pass

class TextEditor:
    def __init__(self):
        self.content = ""
        self.cursor = 0
    
    def insert(self, text: str, position: int = None):
        pos = position if position is not None else self.cursor
        self.content = self.content[:pos] + text + self.content[pos:]
        self.cursor = pos + len(text)
        return pos
    
    def delete(self, start: int, end: int):
        deleted = self.content[start:end]
        self.content = self.content[:start] + self.content[end:]
        self.cursor = start
        return deleted

class InsertAction(Action):
    def __init__(self, editor: TextEditor, text: str, position: int = None):
        self.editor = editor
        self.text = text
        self.position = position
        self.actual_position = None
    
    def execute(self):
        self.actual_position = self.editor.insert(self.text, self.position)
        return self.actual_position
    
    def undo(self):
        if self.actual_position is not None:
            return self.editor.delete(self.actual_position, self.actual_position + len(self.text))
    
    def serialize(self):
        return {
            "type": "insert",
            "text": self.text,
            "position": self.position,
            "timestamp": datetime.now().isoformat()
        }

class DeleteAction(Action):
    def __init__(self, editor: TextEditor, start: int, end: int):
        self.editor = editor
        self.start = start
        self.end = end
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.delete(self.start, self.end)
        return self.deleted_text
    
    def undo(self):
        return self.editor.insert(self.deleted_text, self.start)
    
    def serialize(self):
        return {
            "type": "delete",
            "start": self.start,
            "end": self.end,
            "timestamp": datetime.now().isoformat()
        }

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.executed_actions = []
    
    def execute(self):
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
    
    def undo(self):
        for action in reversed(self.executed_actions):
            action.undo()
        self.executed_actions.clear()
    
    def serialize(self):
        return {
            "type": "macro",
            "actions": [action.serialize() for action in self.actions],
            "timestamp": datetime.now().isoformat()
        }

class Invoker:
    def __init__(self):
        self.history = []
        self.current_position = -1
    
    def execute(self, action: Action):
        self.history = self.history[:self.current_position + 1]
        result = action.execute()
        self.history.append(action)
        self.current_position += 1
        return result
    
    def undo(self):
        if self.current_position >= 0:
            action = self.history[self.current_position]
            result = action.undo()
            self.current_position -= 1
            return result
    
    def redo(self):
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            action = self.history[self.current_position]
            return action.execute()
    
    def save_history(self, filename: str):
        history_data = [action.serialize() for action in self.history[:self.current_position + 1]]
        with open(filename, 'w') as f:
            json.dump(history_data, f, indent=2)

if __name__ == "__main__":
    editor = TextEditor()
    invoker = Invoker()
    
    insert1 = InsertAction(editor, "Hello ", 0)
    insert2 = InsertAction(editor, "World!", None)
    invoker.execute(insert1)
    invoker.execute(insert2)
    print(f"Content: '{editor.content}'")
    
    macro = MacroAction([
        InsertAction(editor, " How", None),
        InsertAction(editor, " are you?", None)
    ])
    invoker.execute(macro)
    print(f"After macro: '{editor.content}'")
    
    invoker.undo()
    print(f"After undo: '{editor.content}'")
    
    invoker.redo()
    print(f"After redo: '{editor.content}'")
    
    delete_action = DeleteAction(editor, 5, 12)
    invoker.execute(delete_action)
    print(f"After delete: '{editor.content}'")
    
    invoker.save_history("editor_history.json")
    print("History saved to file")
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import time

class Action(ABC):
    def __init__(self):
        self.timestamp = time.time()
        self.metadata = {}
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    def can_undo(self) -> bool:
        return True

class TextEditor:
    def __init__(self):
        self.content = ""
    
    def write(self, text: str):
        self.content += text
    
    def delete(self, count: int):
        self.content = self.content[:-count]
    
    def get_content(self) -> str:
        return self.content

class WriteAction(Action):
    def __init__(self, editor: TextEditor, text: str):
        super().__init__()
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.write(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))

class DeleteAction(Action):
    def __init__(self, editor: TextEditor, count: int):
        super().__init__()
        self.editor = editor
        self.count = count
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.get_content()[-self.count:]
        self.editor.delete(self.count)
    
    def undo(self):
        self.editor.write(self.deleted_text)

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        super().__init__()
        self.actions = actions
    
    def execute(self):
        for action in self.actions:
            action.execute()
    
    def undo(self):
        for action in reversed(self.actions):
            if action.can_undo():
                action.undo()

class Processor:
    def __init__(self, max_history: int = 100):
        self.history: List[Action] = []
        self.undo_stack: List[Action] = []
        self.max_history = max_history
    
    def execute(self, action: Action):
        action.execute()
        self.history.append(action)
        self.undo_stack.clear()
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def undo(self) -> bool:
        if not self.history:
            return False
        
        action = self.history.pop()
        if action.can_undo():
            action.undo()
            self.undo_stack.append(action)
            return True
        return False
    
    def redo(self) -> bool:
        if not self.undo_stack:
            return False
        
        action = self.undo_stack.pop()
        action.execute()
        self.history.append(action)
        return True
    
    def get_history_summary(self) -> Dict[str, Any]:
        return {
            'total_actions': len(self.history),
            'can_undo': len(self.history) > 0,
            'can_redo': len(self.undo_stack) > 0,
            'last_action_time': self.history[-1].timestamp if self.history else None
        }

if __name__ == "__main__":
    editor = TextEditor()
    processor = Processor()
    
    write_hello = WriteAction(editor, "Hello ")
    write_world = WriteAction(editor, "World!")
    macro = MacroAction([write_hello, write_world])
    
    processor.execute(macro)
    print(f"After macro: '{editor.get_content()}'")
    
    delete_action = DeleteAction(editor, 6)
    processor.execute(delete_action)
    print(f"After delete: '{editor.get_content()}'")
    
    processor.undo()
    print(f"After undo: '{editor.get_content()}'")
    
    processor.undo()
    print(f"After second undo: '{editor.get_content()}'")
    
    processor.redo()
    print(f"After redo: '{editor.get_content()}'")
    
    print("\nHistory summary:", processor.get_history_summary())
from abc import ABC, abstractmethod
from typing import List, Optional
import copy

class Action(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass
    
    @abstractmethod
    def can_execute(self) -> bool:
        pass

class Document:
    def __init__(self):
        self.content = ""
        self.saved_state = ""
    
    def write(self, text: str) -> None:
        self.content += text
    
    def delete(self, length: int) -> str:
        deleted = self.content[-length:] if length <= len(self.content) else self.content
        self.content = self.content[:-length] if length <= len(self.content) else ""
        return deleted
    
    def save(self) -> None:
        self.saved_state = self.content
    
    def is_saved(self) -> bool:
        return self.content == self.saved_state

class WriteAction(Action):
    def __init__(self, document: Document, text: str):
        self.document = document
        self.text = text
        self.executed = False
    
    def execute(self) -> None:
        if self.can_execute():
            self.document.write(self.text)
            self.executed = True
    
    def undo(self) -> None:
        if self.executed:
            self.document.delete(len(self.text))
            self.executed = False
    
    def can_execute(self) -> bool:
        return not self.executed

class DeleteAction(Action):
    def __init__(self, document: Document, length: int):
        self.document = document
        self.length = length
        self.deleted_text = ""
        self.executed = False
    
    def execute(self) -> None:
        if self.can_execute():
            self.deleted_text = self.document.delete(self.length)
            self.executed = True
    
    def undo(self) -> None:
        if self.executed and self.deleted_text:
            self.document.write(self.deleted_text)
            self.executed = False
    
    def can_execute(self) -> bool:
        return not self.executed and len(self.document.content) >= self.length

class MacroAction(Action):
    def __init__(self, actions: List[Action]):
        self.actions = copy.deepcopy(actions)
        self.executed_actions: List[Action] = []
    
    def execute(self) -> None:
        self.executed_actions.clear()
        for action in self.actions:
            if action.can_execute():
                action.execute()
                self.executed_actions.append(action)
            else:
                break
    
    def undo(self) -> None:
        for action in reversed(self.executed_actions):
            action.undo()
        self.executed_actions.clear()
    
    def can_execute(self) -> bool:
        return any(action.can_execute() for action in self.actions)

class Editor:
    def __init__(self):
        self.history: List[Action] = []
        self.current_position = -1
    
    def execute(self, action: Action) -> bool:
        if action.can_execute():
            action.execute()
            self.history = self.history[:self.current_position + 1]
            self.history.append(action)
            self.current_position += 1
            return True
        return False
    
    def undo(self) -> bool:
        if self.current_position >= 0:
            self.history[self.current_position].undo()
            self.current_position -= 1
            return True
        return False
    
    def redo(self) -> bool:
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            self.history[self.current_position].execute()
            return True
        return False

if __name__ == "__main__":
    doc = Document()
    editor = Editor()
    
    write1 = WriteAction(doc, "Hello ")
    write2 = WriteAction(doc, "World!")
    delete1 = DeleteAction(doc, 6)
    
    editor.execute(write1)
    print(f"After write1: '{doc.content}'")
    
    editor.execute(write2)
    print(f"After write2: '{doc.content}'")
    
    macro = MacroAction([WriteAction(doc, " Python"), WriteAction(doc, " Rocks")])
    editor.execute(macro)
    print(f"After macro: '{doc.content}'")
    
    editor.undo()
    print(f"After undo macro: '{doc.content}'")
    
    editor.redo()
    print(f"After redo: '{doc.content}'")
    
    editor.execute(delete1)
    print(f"After delete: '{doc.content}'")
    
    editor.undo()
    print(f"After undo delete: '{doc.content}'")
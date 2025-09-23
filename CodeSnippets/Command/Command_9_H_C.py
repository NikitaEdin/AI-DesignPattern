from abc import ABC, abstractmethod
from typing import List, Optional
import threading
import time

class Action(ABC):
    def __init__(self, receiver=None):
        self._receiver = receiver
        self._timestamp = time.time()
        self._executed = False
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    @property
    def can_undo(self) -> bool:
        return self._executed

class MacroAction(Action):
    def __init__(self):
        super().__init__()
        self._actions: List[Action] = []
    
    def add(self, action: Action):
        self._actions.append(action)
    
    def execute(self):
        for action in self._actions:
            action.execute()
        self._executed = True
    
    def undo(self):
        if not self.can_undo:
            return
        for action in reversed(self._actions):
            if action.can_undo:
                action.undo()
        self._executed = False

class TextEditor:
    def __init__(self):
        self.content = ""
        self._lock = threading.Lock()
    
    def write(self, text: str):
        with self._lock:
            self.content += text
    
    def delete(self, length: int):
        with self._lock:
            self.content = self.content[:-length]

class WriteAction(Action):
    def __init__(self, editor: TextEditor, text: str):
        super().__init__(editor)
        self._text = text
    
    def execute(self):
        self._receiver.write(self._text)
        self._executed = True
    
    def undo(self):
        if not self.can_undo:
            return
        self._receiver.delete(len(self._text))
        self._executed = False

class DeleteAction(Action):
    def __init__(self, editor: TextEditor, length: int):
        super().__init__(editor)
        self._length = length
        self._deleted_text = ""
    
    def execute(self):
        self._deleted_text = self._receiver.content[-self._length:]
        self._receiver.delete(self._length)
        self._executed = True
    
    def undo(self):
        if not self.can_undo:
            return
        self._receiver.write(self._deleted_text)
        self._executed = False

class Invoker:
    def __init__(self):
        self._history: List[Action] = []
        self._current_index = -1
        self._max_history = 100
    
    def execute(self, action: Action):
        action.execute()
        self._history = self._history[:self._current_index + 1]
        self._history.append(action)
        if len(self._history) > self._max_history:
            self._history.pop(0)
        else:
            self._current_index += 1
    
    def undo(self) -> bool:
        if self._current_index >= 0:
            action = self._history[self._current_index]
            if action.can_undo:
                action.undo()
                self._current_index -= 1
                return True
        return False
    
    def redo(self) -> bool:
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            action = self._history[self._current_index]
            action.execute()
            return True
        return False

if __name__ == "__main__":
    editor = TextEditor()
    invoker = Invoker()
    
    write_hello = WriteAction(editor, "Hello ")
    write_world = WriteAction(editor, "World!")
    
    macro = MacroAction()
    macro.add(write_hello)
    macro.add(write_world)
    
    invoker.execute(macro)
    print(f"After macro: '{editor.content}'")
    
    delete_action = DeleteAction(editor, 6)
    invoker.execute(delete_action)
    print(f"After delete: '{editor.content}'")
    
    invoker.undo()
    print(f"After undo: '{editor.content}'")
    
    invoker.undo()
    print(f"After second undo: '{editor.content}'")
    
    invoker.redo()
    print(f"After redo: '{editor.content}'")
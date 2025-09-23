from abc import ABC, abstractmethod
from typing import List

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class TextEditor:
    def __init__(self):
        self.content = ""
    
    def write(self, text):
        self.content += text
    
    def delete(self, count):
        self.content = self.content[:-count]
    
    def get_content(self):
        return self.content

class WriteOperation(Action):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.write(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))

class DeleteOperation(Action):
    def __init__(self, editor, count):
        self.editor = editor
        self.count = count
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.get_content()[-self.count:]
        self.editor.delete(self.count)
    
    def undo(self):
        self.editor.write(self.deleted_text)

class EditorInvoker:
    def __init__(self):
        self.history: List[Action] = []
        self.current_position = -1
    
    def execute_action(self, action):
        action.execute()
        self.history = self.history[:self.current_position + 1]
        self.history.append(action)
        self.current_position += 1
    
    def undo(self):
        if self.current_position >= 0:
            self.history[self.current_position].undo()
            self.current_position -= 1
            return True
        return False

if __name__ == "__main__":
    editor = TextEditor()
    invoker = EditorInvoker()
    
    write1 = WriteOperation(editor, "Hello ")
    write2 = WriteOperation(editor, "World!")
    delete1 = DeleteOperation(editor, 6)
    
    invoker.execute_action(write1)
    print(f"After write 'Hello ': {editor.get_content()}")
    
    invoker.execute_action(write2)
    print(f"After write 'World!': {editor.get_content()}")
    
    invoker.execute_action(delete1)
    print(f"After delete 6 chars: {editor.get_content()}")
    
    invoker.undo()
    print(f"After undo: {editor.get_content()}")
    
    invoker.undo()
    print(f"After second undo: {editor.get_content()}")
class TextEditor:
    def __init__(self):
        self.content = ""
    
    def write(self, text):
        self.content += text
    
    def delete(self, length):
        self.content = self.content[:-length]
    
    def get_content(self):
        return self.content

class Action:
    def execute(self):
        raise NotImplementedError
    
    def undo(self):
        raise NotImplementedError

class WriteAction(Action):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.write(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))

class DeleteAction(Action):
    def __init__(self, editor, length):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.content[-self.length:]
        self.editor.delete(self.length)
    
    def undo(self):
        self.editor.write(self.deleted_text)

class EditorInvoker:
    def __init__(self):
        self.history = []
    
    def execute_action(self, action):
        action.execute()
        self.history.append(action)
    
    def undo_last(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()

if __name__ == "__main__":
    editor = TextEditor()
    invoker = EditorInvoker()
    
    write1 = WriteAction(editor, "Hello ")
    write2 = WriteAction(editor, "World!")
    delete1 = DeleteAction(editor, 6)
    
    invoker.execute_action(write1)
    print(f"After write: '{editor.get_content()}'")
    
    invoker.execute_action(write2)
    print(f"After write: '{editor.get_content()}'")
    
    invoker.execute_action(delete1)
    print(f"After delete: '{editor.get_content()}'")
    
    invoker.undo_last()
    print(f"After undo: '{editor.get_content()}'")
    
    invoker.undo_last()
    print(f"After undo: '{editor.get_content()}'")
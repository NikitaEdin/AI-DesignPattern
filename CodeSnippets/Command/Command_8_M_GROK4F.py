from abc import ABC, abstractmethod

class TextBuffer:
    def __init__(self):
        self.content = []

    def insert(self, pos, text):
        if pos < 0:
            raise ValueError("Position cannot be negative")
        self.content[pos:pos] = list(text)

    def delete(self, pos, length):
        if pos < 0 or length <= 0:
            raise ValueError("Invalid delete parameters")
        start = pos
        end = min(start + length, len(self.content))
        deleted = ''.join(self.content[start:end])
        del self.content[start:end]
        return deleted

    def __str__(self):
        return ''.join(self.content)

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class InsertAction(Action):
    def __init__(self, buffer, pos, text):
        self.buffer = buffer
        self.pos = pos
        self.text = text

    def execute(self):
        self.buffer.insert(self.pos, self.text)

    def undo(self):
        start = self.pos
        end = start + len(self.text)
        if end <= len(self.buffer.content):
            del self.buffer.content[start:end]

class DeleteAction(Action):
    def __init__(self, buffer, pos, length):
        self.buffer = buffer
        self.pos = pos
        self.length = length
        self.deleted_text = None

    def execute(self):
        self.deleted_text = self.buffer.delete(self.pos, self.length)

    def undo(self):
        if self.deleted_text:
            self.buffer.insert(self.pos, self.deleted_text)

class EditorController:
    def __init__(self, buffer):
        self.buffer = buffer
        self.undo_stack = []

    def perform(self, action):
        try:
            action.execute()
            self.undo_stack.append(action)
        except ValueError as e:
            print(f"Execution error: {e}")

    def undo_last(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            action.undo()
        else:
            print("No actions to undo")

if __name__ == "__main__":
    buffer = TextBuffer()
    controller = EditorController(buffer)

    insert1 = InsertAction(buffer, 0, "Hello")
    controller.perform(insert1)
    print(str(buffer))  # Hello

    insert2 = InsertAction(buffer, 5, " world")
    controller.perform(insert2)
    print(str(buffer))  # Hello world

    delete = DeleteAction(buffer, 5, 6)
    controller.perform(delete)
    print(str(buffer))  # Hello

    controller.undo_last()
    print(str(buffer))  # Hello world

    controller.undo_last()
    print(str(buffer))  # Hello
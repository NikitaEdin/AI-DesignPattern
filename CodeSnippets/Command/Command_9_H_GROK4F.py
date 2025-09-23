import abc

class Buffer:
    def __init__(self):
        self.content = []
        self.cursor = 0

    def insert(self, text, position=None):
        if position is None:
            position = self.cursor
        self.content.insert(position, text)
        self.cursor = position + 1

    def delete(self, count=1, position=None):
        if position is None:
            position = self.cursor
        for _ in range(min(count, len(self.content) - position)):
            del self.content[position]
        self.cursor = max(0, position - count)

    def get_content(self):
        return ''.join(self.content)

class Operation(abc.ABC):
    def __init__(self, buffer):
        self.buffer = buffer
        self.executed = False

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

class InsertText(Operation):
    def __init__(self, buffer, text, position=None):
        super().__init__(buffer)
        self.text = text
        self.position = position if position is not None else buffer.cursor
        self.previous_cursor = buffer.cursor

    def execute(self):
        if not self.executed:
            self.buffer.insert(self.text, self.position)
            self.executed = True

    def undo(self):
        if self.executed:
            self.buffer.delete(len(self.text), self.position)
            self.buffer.cursor = self.previous_cursor
            self.executed = False

class DeleteText(Operation):
    def __init__(self, buffer, count=1, position=None):
        super().__init__(buffer)
        self.count = count
        self.position = position if position is not None else buffer.cursor
        self.deleted_text = self.buffer.content[self.position:self.position + count]
        self.previous_cursor = self.buffer.cursor

    def execute(self):
        if not self.executed:
            self.buffer.delete(self.count, self.position)
            self.executed = True

    def undo(self):
        if self.executed:
            insert_pos = self.position
            for char in self.deleted_text:
                self.buffer.insert(char, insert_pos)
                insert_pos += 1
            self.buffer.cursor = self.previous_cursor
            self.executed = False

class Application:
    def __init__(self):
        self.buffer = Buffer()
        self.history = []
        self.redo_stack = []

    def perform(self, operation):
        if len(self.history) > 0:
            self.redo_stack.clear()
        operation.execute()
        self.history.append(operation)

    def undo(self):
        if self.history:
            last_op = self.history.pop()
            last_op.undo()
            self.redo_stack.append(last_op)
        else:
            print("No actions to undo.")

    def redo(self):
        if self.redo_stack:
            op = self.redo_stack.pop()
            op.execute()
            self.history.append(op)
        else:
            print("No actions to redo.")

    def display(self):
        print(f"Content: '{self.buffer.get_content()}'")

if __name__ == "__main__":
    app = Application()
    app.display()

    insert1 = InsertText(app.buffer, "Hello")
    app.perform(insert1)
    app.display()

    insert2 = InsertText(app.buffer, ", World!")
    app.perform(insert2)
    app.display()

    app.undo()
    app.display()

    app.redo()
    app.display()

    delete = DeleteText(app.buffer, count=5)
    app.perform(delete)
    app.display()

    app.undo()
    app.display()
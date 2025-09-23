import abc
from typing import List

class OperationBase(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None:
        pass
    @abc.abstractmethod
    def undo(self) -> None:
        pass

class Document:
    def __init__(self, text: str = ""):
        self.text = text
    def insert(self, pos: int, content: str):
        if pos < 0 or pos > len(self.text):
            raise ValueError("Position out of range")
        self.text = self.text[:pos] + content + self.text[pos:]
    def remove(self, pos: int, length: int):
        if pos < 0 or pos + length > len(self.text):
            raise ValueError("Removal out of range")
        removed = self.text[pos:pos+length]
        self.text = self.text[:pos] + self.text[pos+length:]
        return removed

class InsertOperation(OperationBase):
    def __init__(self, receiver: Document, pos: int, content: str):
        self.receiver = receiver
        self.pos = pos
        self.content = content
        self.executed = False
    def execute(self):
        if self.executed:
            raise RuntimeError("Already executed")
        self.receiver.insert(self.pos, self.content)
        self.executed = True
    def undo(self):
        if not self.executed:
            raise RuntimeError("Nothing to undo")
        self.receiver.remove(self.pos, len(self.content))
        self.executed = False

class RemoveOperation(OperationBase):
    def __init__(self, receiver: Document, pos: int, length: int):
        self.receiver = receiver
        self.pos = pos
        self.length = length
        self.backup = None
        self.executed = False
    def execute(self):
        if self.executed:
            raise RuntimeError("Already executed")
        self.backup = self.receiver.remove(self.pos, self.length)
        self.executed = True
    def undo(self):
        if not self.executed:
            raise RuntimeError("Nothing to undo")
        self.receiver.insert(self.pos, self.backup)
        self.executed = False

class OperationInvoker:
    def __init__(self):
        self.history: List[OperationBase] = []
    def run(self, op: OperationBase):
        try:
            op.execute()
            self.history.append(op)
        except Exception as e:
            print(f"Execution failed: {e}")
    def undo_last(self):
        if not self.history:
            print("Nothing to undo")
            return
        op = self.history.pop()
        try:
            op.undo()
        except Exception as e:
            print(f"Undo failed: {e}")

def main():
    doc = Document("Hello World")
    invoker = OperationInvoker()
    insert_op = InsertOperation(doc, 5, ", Cruel")
    remove_op = RemoveOperation(doc, 0, 6)
    print(doc.text)
    invoker.run(insert_op)
    print(doc.text)
    invoker.run(remove_op)
    print(doc.text)
    invoker.undo_last()
    print(doc.text)
    invoker.undo_last()
    print(doc.text)
    invoker.undo_last()

if __name__ == "__main__":
    main()
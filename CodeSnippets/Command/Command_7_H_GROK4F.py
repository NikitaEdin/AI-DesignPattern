from abc import ABC, abstractmethod
from typing import List

class TextBuffer:
    def __init__(self):
        self.content = []
    
    def insert_at(self, position: int, text: str):
        if 0 <= position <= len(self.content):
            self.content.insert(position, text)
        else:
            raise ValueError("Invalid position")
    
    def delete_at(self, position: int, length: int = 1):
        if 0 <= position < len(self.content) and length > 0:
            deleted = self.content[position:position + length]
            del self.content[position:position + length]
            return deleted
        raise ValueError("Invalid deletion parameters")
    
    def get_content(self) -> str:
        return ' '.join(self.content)

class Executable(ABC):
    @abstractmethod
    def perform(self):
        pass
    
    @abstractmethod
    def reverse(self):
        pass

class InsertOperation(Executable):
    def __init__(self, buffer: TextBuffer, position: int, text: str):
        self.buffer = buffer
        self.position = position
        self.text = text
        self.was_inserted = False
    
    def perform(self):
        try:
            self.buffer.insert_at(self.position, self.text)
            self.was_inserted = True
        except ValueError as e:
            print(f"Insertion failed: {e}")
    
    def reverse(self):
        if self.was_inserted:
            try:
                deleted = self.buffer.delete_at(self.position, 1)
                if deleted and deleted[0] != self.text:
                    self.buffer.insert_at(self.position, self.text)
            except ValueError:
                pass
        self.was_inserted = False

class DeleteOperation(Executable):
    def __init__(self, buffer: TextBuffer, position: int, length: int = 1):
        self.buffer = buffer
        self.position = position
        self.length = length
        self.deleted_text = None
        self.was_deleted = False
    
    def perform(self):
        try:
            self.deleted_text = self.buffer.delete_at(self.position, self.length)
            self.was_deleted = self.deleted_text is not None
        except ValueError as e:
            print(f"Deletion failed: {e}")
    
    def reverse(self):
        if self.was_deleted and self.deleted_text:
            try:
                for item in reversed(self.deleted_text):
                    self.buffer.insert_at(self.position, item)
            except ValueError:
                pass
        self.was_deleted = False

class SequenceExecutable(Executable):
    def __init__(self):
        self.sub_operations: List[Executable] = []
    
    def add(self, operation: Executable):
        if operation:
            self.sub_operations.append(operation)
    
    def perform(self):
        for op in self.sub_operations:
            try:
                op.perform()
            except Exception:
                # Rollback previous on failure
                for prev_op in reversed(self.sub_operations[:self.sub_operations.index(op)]):
                    prev_op.reverse()
                raise
    
    def reverse(self):
        for op in reversed(self.sub_operations):
            op.reverse()

class TaskProcessor:
    def __init__(self):
        self.history: List[Executable] = []
    
    def execute(self, operation: Executable):
        if operation:
            try:
                operation.perform()
                self.history.append(operation)
            except Exception as e:
                print(f"Execution failed: {e}")
    
    def undo_last(self):
        if self.history:
            last = self.history.pop()
            last.reverse()
        else:
            print("No operations to undo")

if __name__ == "__main__":
    buffer = TextBuffer()
    processor = TaskProcessor()
    
    # Simple operations
    insert1 = InsertOperation(buffer, 0, "Hello")
    processor.execute(insert1)
    insert2 = InsertOperation(buffer, 1, "World")
    processor.execute(insert2)
    print(f"Content: {buffer.get_content()}")
    
    # Undo last
    processor.undo_last()
    print(f"After undo: {buffer.get_content()}")
    
    # Composite
    seq = SequenceExecutable()
    seq.add(InsertOperation(buffer, 0, "Python"))
    seq.add(DeleteOperation(buffer, 1, 1))
    processor.execute(seq)
    print(f"After sequence: {buffer.get_content()}")
    
    # Undo composite
    processor.undo_last()
    print(f"After undo sequence: {buffer.get_content()}")
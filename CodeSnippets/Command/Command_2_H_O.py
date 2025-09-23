from abc import ABC, abstractmethod
from typing import List, Any


class ActionBase(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class TextEditor:
    def __init__(self, content: str = ""):
        self.content = content

    def insert(self, pos: int, text: str) -> None:
        if not (0 <= pos <= len(self.content)):
            raise IndexError("Insert position out of range")
        self.content = self.content[:pos] + text + self.content[pos:]

    def delete(self, pos: int, length: int) -> str:
        if not (0 <= pos <= len(self.content)) or length < 0 or pos + length > len(self.content):
            raise IndexError("Delete range out of bounds")
        deleted = self.content[pos:pos + length]
        self.content = self.content[:pos] + self.content[pos + length:]
        return deleted

    def replace(self, pos: int, length: int, text: str) -> str:
        deleted = self.delete(pos, length)
        self.insert(pos, text)
        return deleted


class InsertAction(ActionBase):
    def __init__(self, receiver: TextEditor, pos: int, text: str):
        self.receiver = receiver
        self.pos = pos
        self.text = text
        self.executed = False

    def execute(self) -> None:
        self.receiver.insert(self.pos, self.text)
        self.executed = True

    def undo(self) -> None:
        if not self.executed:
            return
        self.receiver.delete(self.pos, len(self.text))
        self.executed = False


class DeleteAction(ActionBase):
    def __init__(self, receiver: TextEditor, pos: int, length: int):
        self.receiver = receiver
        self.pos = pos
        self.length = length
        self.deleted_text: str | None = None

    def execute(self) -> None:
        self.deleted_text = self.receiver.delete(self.pos, self.length)

    def undo(self) -> None:
        if self.deleted_text is None:
            return
        self.receiver.insert(self.pos, self.deleted_text)
        self.deleted_text = None


class ReplaceAction(ActionBase):
    def __init__(self, receiver: TextEditor, pos: int, length: int, text: str):
        self.receiver = receiver
        self.pos = pos
        self.length = length
        self.text = text
        self.old_text: str | None = None

    def execute(self) -> None:
        self.old_text = self.receiver.replace(self.pos, self.length, self.text)

    def undo(self) -> None:
        if self.old_text is None:
            return
        self.receiver.replace(self.pos, len(self.text), self.old_text)
        self.old_text = None


class GroupAction(ActionBase):
    def __init__(self, actions: List[ActionBase]):
        self.actions = list(actions)
        self.performed: List[ActionBase] = []

    def execute(self) -> None:
        self.performed = []
        try:
            for a in self.actions:
                a.execute()
                self.performed.append(a)
        except Exception as e:
            for executed in reversed(self.performed):
                try:
                    executed.undo()
                except Exception:
                    pass
            self.performed = []
            raise e

    def undo(self) -> None:
        for a in reversed(self.performed):
            try:
                a.undo()
            except Exception:
                pass
        self.performed = []


class Executor:
    def __init__(self):
        self.done: List[ActionBase] = []
        self.undone: List[ActionBase] = []

    def perform(self, action: ActionBase) -> None:
        action.execute()
        self.done.append(action)
        self.undone.clear()

    def undo(self) -> None:
        if not self.done:
            raise IndexError("Nothing to undo")
        action = self.done.pop()
        action.undo()
        self.undone.append(action)

    def redo(self) -> None:
        if not self.undone:
            raise IndexError("Nothing to redo")
        action = self.undone.pop()
        action.execute()
        self.done.append(action)

    def clear_history(self) -> None:
        self.done.clear()
        self.undone.clear()


if __name__ == "__main__":
    editor = TextEditor("Hello World")
    execer = Executor()

    a1 = InsertAction(editor, 5, ",")
    a2 = InsertAction(editor, 6, " dear")
    a3 = DeleteAction(editor, 11, 5)
    group = GroupAction([a1, a2, a3])

    execer.perform(group)
    print(editor.content)

    execer.undo()
    print(editor.content)

    execer.redo()
    print(editor.content)

    r1 = ReplaceAction(editor, 0, 5, "Hi")
    execer.perform(r1)
    print(editor.content)

    execer.undo()
    print(editor.content)
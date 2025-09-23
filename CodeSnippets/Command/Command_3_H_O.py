from abc import ABC, abstractmethod
from typing import List, Optional


class TextEditor:
    def __init__(self, content: str = ""):
        self._content = content

    def insert(self, text: str, pos: Optional[int] = None) -> None:
        if pos is None:
            pos = len(self._content)
        if pos < 0 or pos > len(self._content):
            raise IndexError("Insert position out of range")
        self._content = self._content[:pos] + text + self._content[pos:]

    def delete(self, start: int, end: int) -> str:
        if start < 0 or end > len(self._content) or start >= end:
            raise IndexError("Invalid delete range")
        removed = self._content[start:end]
        self._content = self._content[:start] + self._content[end:]
        return removed

    def replace(self, start: int, end: int, text: str) -> str:
        removed = self.delete(start, end)
        self.insert(text, start)
        return removed

    def content(self) -> str:
        return self._content


class Operation(ABC):
    def __init__(self):
        self._done = False

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class InsertAction(Operation):
    def __init__(self, editor: TextEditor, text: str, pos: Optional[int] = None):
        super().__init__()
        self.editor = editor
        self.text = text
        self.pos = pos if pos is not None else None
        self._actual_pos: Optional[int] = None

    def execute(self) -> None:
        if self._done:
            raise RuntimeError("Already executed")
        pos = self.pos if self.pos is not None else len(self.editor.content())
        self.editor.insert(self.text, pos)
        self._actual_pos = pos
        self._done = True

    def undo(self) -> None:
        if not self._done or self._actual_pos is None:
            raise RuntimeError("Nothing to undo")
        start = self._actual_pos
        end = start + len(self.text)
        self.editor.delete(start, end)
        self._done = False


class DeleteAction(Operation):
    def __init__(self, editor: TextEditor, start: int, end: int):
        super().__init__()
        self.editor = editor
        self.start = start
        self.end = end
        self._removed: Optional[str] = None

    def execute(self) -> None:
        if self._done:
            raise RuntimeError("Already executed")
        self._removed = self.editor.delete(self.start, self.end)
        self._done = True

    def undo(self) -> None:
        if not self._done or self._removed is None:
            raise RuntimeError("Nothing to undo")
        self.editor.insert(self._removed, self.start)
        self._done = False


class ReplaceAction(Operation):
    def __init__(self, editor: TextEditor, start: int, end: int, text: str):
        super().__init__()
        self.editor = editor
        self.start = start
        self.end = end
        self.text = text
        self._original: Optional[str] = None

    def execute(self) -> None:
        if self._done:
            raise RuntimeError("Already executed")
        self._original = self.editor.replace(self.start, self.end, self.text)
        self._done = True

    def undo(self) -> None:
        if not self._done or self._original is None:
            raise RuntimeError("Nothing to undo")
        cur_end = self.start + len(self.text)
        self.editor.replace(self.start, cur_end, self._original)
        self._done = False


class MacroAction(Operation):
    def __init__(self, actions: List[Operation]):
        super().__init__()
        self.actions = actions
        self._executed_count = 0

    def execute(self) -> None:
        if self._done:
            raise RuntimeError("Already executed")
        try:
            for act in self.actions:
                act.execute()
                self._executed_count += 1
        except Exception:
            for executed in reversed(self.actions[: self._executed_count]):
                try:
                    executed.undo()
                except Exception:
                    pass
            self._executed_count = 0
            raise
        self._done = True

    def undo(self) -> None:
        if not self._done:
            raise RuntimeError("Nothing to undo")
        for act in reversed(self.actions[: self._executed_count]):
            act.undo()
        self._executed_count = 0
        self._done = False


class Controller:
    def __init__(self):
        self._history: List[Operation] = []
        self._redo_stack: List[Operation] = []

    def perform(self, op: Operation) -> None:
        op.execute()
        self._history.append(op)
        self._redo_stack.clear()

    def perform_batch(self, ops: List[Operation]) -> None:
        executed: List[Operation] = []
        try:
            for op in ops:
                op.execute()
                executed.append(op)
            self._history.extend(executed)
            self._redo_stack.clear()
        except Exception:
            for op in reversed(executed):
                try:
                    op.undo()
                except Exception:
                    pass
            raise

    def undo(self, steps: int = 1) -> None:
        for _ in range(steps):
            if not self._history:
                raise RuntimeError("Nothing to undo")
            op = self._history.pop()
            op.undo()
            self._redo_stack.append(op)

    def redo(self, steps: int = 1) -> None:
        for _ in range(steps):
            if not self._redo_stack:
                raise RuntimeError("Nothing to redo")
            op = self._redo_stack.pop()
            op.execute()
            self._history.append(op)


if __name__ == "__main__":
    editor = TextEditor("Hello")
    controller = Controller()

    a1 = InsertAction(editor, ", world")
    controller.perform(a1)
    a2 = InsertAction(editor, "!", None)
    controller.perform(a2)

    print(editor.content())

    a3 = DeleteAction(editor, 5, 6)
    controller.perform(a3)
    print(editor.content())

    macro = MacroAction([ReplaceAction(editor, 0, 5, "Hi"), InsertAction(editor, " :)")])
    try:
        controller.perform(macro)
    except Exception as e:
        print("Macro failed:", e)
    print(editor.content())

    controller.undo(2)
    print("After undo x2:", editor.content())

    controller.redo(2)
    print("After redo x2:", editor.content())

    failing = ReplaceAction(editor, 100, 101, "X")
    try:
        controller.perform_batch([InsertAction(editor, " BEGIN "), failing, InsertAction(editor, " END ")])
    except Exception as e:
        print("Batch rolled back due to:", e)
    print("Final content:", editor.content())
from abc import ABC, abstractmethod
from typing import List, Callable, Optional


class ActionError(Exception):
    pass


class ActionBase(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


class MacroAction(ActionBase):
    def __init__(self, actions: Optional[List[ActionBase]] = None):
        self._actions: List[ActionBase] = list(actions) if actions else []

    def add(self, action: ActionBase) -> None:
        self._actions.append(action)

    def execute(self) -> None:
        executed: List[ActionBase] = []
        try:
            for a in self._actions:
                a.execute()
                executed.append(a)
        except Exception as exc:
            for e in reversed(executed):
                try:
                    e.undo()
                except Exception:
                    pass
            raise ActionError("Macro execution failed") from exc

    def undo(self) -> None:
        for a in reversed(self._actions):
            a.undo()


class Controller:
    def __init__(self, history_limit: int = 100):
        self._undo_stack: List[ActionBase] = []
        self._redo_stack: List[ActionBase] = []
        self._limit = max(1, int(history_limit))

    def run(self, action: ActionBase) -> None:
        try:
            action.execute()
        except Exception as exc:
            raise ActionError("Action failed to run") from exc
        self._undo_stack.append(action)
        if len(self._undo_stack) > self._limit:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._undo_stack:
            raise ActionError("Nothing to undo")
        action = self._undo_stack.pop()
        try:
            action.undo()
        except Exception as exc:
            raise ActionError("Undo failed") from exc
        self._redo_stack.append(action)

    def redo(self) -> None:
        if not self._redo_stack:
            raise ActionError("Nothing to redo")
        action = self._redo_stack.pop()
        try:
            action.execute()
        except Exception as exc:
            raise ActionError("Redo failed") from exc
        self._undo_stack.append(action)


class TextDocument:
    def __init__(self, text: str = ""):
        self.text = text

    def insert(self, pos: int, content: str) -> None:
        if pos < 0 or pos > len(self.text):
            raise IndexError("Position out of bounds")
        self.text = self.text[:pos] + content + self.text[pos:]

    def delete(self, pos: int, length: int) -> str:
        if pos < 0 or pos + length > len(self.text):
            raise IndexError("Delete range out of bounds")
        removed = self.text[pos : pos + length]
        self.text = self.text[:pos] + self.text[pos + length :]
        return removed

    def replace(self, pos: int, length: int, content: str) -> str:
        removed = self.delete(pos, length)
        self.insert(pos, content)
        return removed


class InsertText(ActionBase):
    def __init__(self, doc: TextDocument, pos: int, content: str):
        self.doc = doc
        self.pos = pos
        self.content = content
        self._executed = False

    def execute(self) -> None:
        if self._executed:
            raise ActionError("Already executed")
        self.doc.insert(self.pos, self.content)
        self._executed = True

    def undo(self) -> None:
        if not self._executed:
            raise ActionError("Cannot undo before execute")
        self.doc.delete(self.pos, len(self.content))
        self._executed = False


class ReplaceText(ActionBase):
    def __init__(self, doc: TextDocument, pos: int, length: int, content: str):
        self.doc = doc
        self.pos = pos
        self.length = length
        self.content = content
        self._previous: Optional[str] = None

    def execute(self) -> None:
        if self._previous is not None:
            raise ActionError("Already executed")
        self._previous = self.doc.replace(self.pos, self.length, self.content)

    def undo(self) -> None:
        if self._previous is None:
            raise ActionError("Cannot undo before execute")
        self.doc.replace(self.pos, len(self.content), self._previous)
        self._previous = None


class FunctionAction(ActionBase):
    def __init__(self, do: Callable[[], None], undo: Callable[[], None]):
        self._do = do
        self._undo = undo
        self._done = False

    def execute(self) -> None:
        if self._done:
            raise ActionError("Already executed")
        self._do()
        self._done = True

    def undo(self) -> None:
        if not self._done:
            raise ActionError("Cannot undo before execute")
        self._undo()
        self._done = False


if __name__ == "__main__":
    doc = TextDocument("Hello")
    ctrl = Controller(history_limit=10)

    a1 = InsertText(doc, 5, " World")
    a2 = ReplaceText(doc, 0, 5, "Hi")
    macro = MacroAction([a1, a2])

    ctrl.run(macro)
    print(doc.text)

    ctrl.undo()
    print(doc.text)

    ctrl.redo()
    print(doc.text)

    def do_upper():
        doc.text = doc.text.upper()

    def undo_upper():
        doc.text = doc.text.lower().capitalize()

    fa = FunctionAction(do_upper, undo_upper)
    ctrl.run(fa)
    print(doc.text)

    ctrl.undo()
    print(doc.text)
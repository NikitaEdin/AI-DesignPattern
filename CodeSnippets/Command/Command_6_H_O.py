from abc import ABC, abstractmethod

class Document:
    def __init__(self, text=""):
        self._text = text

    def insert(self, pos, segment):
        if pos < 0 or pos > len(self._text):
            raise IndexError("Insert position out of range")
        self._text = self._text[:pos] + segment + self._text[pos:]

    def remove(self, pos, length):
        if pos < 0 or pos + length > len(self._text):
            raise IndexError("Remove range out of range")
        removed = self._text[pos:pos+length]
        self._text = self._text[:pos] + self._text[pos+length:]
        return removed

    def text(self):
        return self._text

class ActionBase(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class InsertAction(ActionBase):
    def __init__(self, doc, pos, content):
        self.doc = doc
        self.pos = pos
        self.content = content
        self._executed = False

    def execute(self):
        self.doc.insert(self.pos, self.content)
        self._executed = True

    def undo(self):
        if not self._executed:
            return
        self.doc.remove(self.pos, len(self.content))
        self._executed = False

class DeleteAction(ActionBase):
    def __init__(self, doc, pos, length):
        self.doc = doc
        self.pos = pos
        self.length = length
        self._backup = None
        self._executed = False

    def execute(self):
        self._backup = self.doc.remove(self.pos, self.length)
        self._executed = True

    def undo(self):
        if not self._executed:
            return
        self.doc.insert(self.pos, self._backup)
        self._executed = False
        self._backup = None

class GroupAction(ActionBase):
    def __init__(self, actions):
        self.actions = list(actions)
        self._executed_count = 0

    def execute(self):
        self._executed_count = 0
        try:
            for a in self.actions:
                a.execute()
                self._executed_count += 1
        except Exception:
            for i in range(self._executed_count - 1, -1, -1):
                try:
                    self.actions[i].undo()
                except Exception:
                    pass
            self._executed_count = 0
            raise

    def undo(self):
        for a in reversed(self.actions[:self._executed_count]):
            try:
                a.undo()
            except Exception:
                pass
        self._executed_count = 0

class Controller:
    def __init__(self):
        self._history = []
        self._position = 0

    def perform(self, action):
        try:
            action.execute()
        except Exception:
            raise
        else:
            if self._position < len(self._history):
                self._history = self._history[:self._position]
            self._history.append(action)
            self._position += 1

    def undo(self):
        if self._position == 0:
            return False
        action = self._history[self._position - 1]
        try:
            action.undo()
        except Exception:
            raise
        else:
            self._position -= 1
            return True

    def redo(self):
        if self._position >= len(self._history):
            return False
        action = self._history[self._position]
        try:
            action.execute()
        except Exception:
            raise
        else:
            self._position += 1
            return True

if __name__ == "__main__":
    doc = Document("Hello")
    ctrl = Controller()

    a1 = InsertAction(doc, 5, ", world")
    ctrl.perform(a1)
    print(doc.text())

    a2 = InsertAction(doc, 0, "Say: ")
    ctrl.perform(a2)
    print(doc.text())

    ctrl.undo()
    print("after undo:", doc.text())

    ctrl.redo()
    print("after redo:", doc.text())

    d1 = DeleteAction(doc, 0, 5)
    d2 = InsertAction(doc, 0, "Hi")
    group = GroupAction([d1, d2])
    ctrl.perform(group)
    print("after group:", doc.text())

    ctrl.undo()
    print("after group undo:", doc.text())

    try:
        bad = DeleteAction(doc, 100, 1)
        ctrl.perform(bad)
    except Exception as e:
        print("caught error:", e)
    print("final:", doc.text())
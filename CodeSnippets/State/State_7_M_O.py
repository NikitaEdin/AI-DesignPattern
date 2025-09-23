from abc import ABC, abstractmethod

class ModeBase(ABC):
    @abstractmethod
    def handle(self, context, action):
        pass

    @property
    @abstractmethod
    def label(self):
        pass

class DraftMode(ModeBase):
    @property
    def label(self):
        return "draft"

    def handle(self, context, action):
        if action == "edit":
            context.content += " [edited]"
            return "Edited in draft"
        if action == "publish":
            context.switch_mode(PublishedMode())
            return "Published"
        raise RuntimeError(f"Action '{action}' not allowed in draft")

class PublishedMode(ModeBase):
    @property
    def label(self):
        return "published"

    def handle(self, context, action):
        if action == "view":
            return f"Viewing: {context.content}"
        if action == "archive":
            context.switch_mode(ArchivedMode())
            return "Archived"
        raise RuntimeError(f"Action '{action}' not allowed when published")

class ArchivedMode(ModeBase):
    @property
    def label(self):
        return "archived"

    def handle(self, context, action):
        if action == "restore":
            context.switch_mode(DraftMode())
            return "Restored to draft"
        raise RuntimeError(f"Action '{action}' not allowed when archived")

class DocumentContext:
    def __init__(self, title, initial_mode):
        if not isinstance(initial_mode, ModeBase):
            raise TypeError("initial_mode must implement ModeBase")
        self.title = title
        self.content = ""
        self._current = initial_mode
        self._history = []

    def switch_mode(self, new_mode):
        if not isinstance(new_mode, ModeBase):
            raise TypeError("new_mode must implement ModeBase")
        self._history.append(self._current)
        self._current = new_mode

    def revert_mode(self):
        if not self._history:
            raise RuntimeError("No previous mode to revert to")
        self._current = self._history.pop()

    def perform(self, action):
        try:
            result = self._current.handle(self, action)
            return {"status": "ok", "mode": self._current.label, "result": result}
        except Exception as exc:
            return {"status": "error", "mode": self._current.label, "error": str(exc)}

if __name__ == "__main__":
    doc = DocumentContext("Report", DraftMode())
    print(doc.perform("edit"))
    print(doc.perform("publish"))
    print(doc.perform("view"))
    print(doc.perform("archive"))
    print(doc.perform("restore"))
    print(doc.perform("edit"))
    print("Reverting previous mode...")
    try:
        doc.revert_mode()
        print("Reverted to", doc._current.label)
    except RuntimeError as e:
        print("Revert failed:", e)
    print(doc.perform("publish"))
from abc import ABC, abstractmethod

class Context:
    def __init__(self):
        self._current = Draft()
    def set_mode(self, mode):
        self._current = mode
    def publish(self):
        self._current.publish(self)
    def expire(self):
        self._current.expire(self)

class Mode(ABC):
    @abstractmethod
    def publish(self, ctx): pass
    @abstractmethod
    def expire(self, ctx): pass

class Draft(Mode):
    def publish(self, ctx):
        ctx.set_mode(Published())
    def expire(self, ctx):
        raise RuntimeError("Draft cannot expire")

class Published(Mode):
    def publish(self, ctx):
        raise RuntimeError("Already published")
    def expire(self, ctx):
        ctx.set_mode(Archived())

class Archived(Mode):
    def publish(self, ctx):
        raise RuntimeError("Archived items can’t be republished")
    def expire(self, ctx): pass

if __name__ == "__main__":
    doc = Context()
    doc.publish()
    try: doc.publish()
    except: pass
    doc.expire()
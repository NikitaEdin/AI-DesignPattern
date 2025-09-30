from abc import ABC, abstractmethod

class Mode(ABC):
    @abstractmethod
    def handle(self, ctx): pass
    @abstractmethod
    def change(self, ctx): pass

class ModeA(Mode):
    def handle(self, ctx): print("ModeA handling")
    def change(self, ctx): ctx.mode = ctx.b

class ModeB(Mode):
    def handle(self, ctx): print("ModeB handling")
    def change(self, ctx): ctx.mode = ctx.a

class Context:
    def __init__(self):
        self.a, self.b = ModeA(), ModeB()
        self.mode = self.a
    def request(self):
        self.mode.handle(self)
    def switch(self):
        self.mode.change(self)

if __name__ == "__main__":
    c = Context()
    c.request()
    c.switch()
    c.request()
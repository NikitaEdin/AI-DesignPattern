class Context:
    def __init__(self, initial):
        self._current = initial
        self._current.enter(self)
    def request(self):
        self._current.handle(self)
class ModeA:
    def enter(self, ctx): print("Entering A")
    def handle(self, ctx):
        print("Handling in A -> switching to B")
        ctx._current = ModeB()
        ctx._current.enter(ctx)
class ModeB:
    def enter(self, ctx): print("Entering B")
    def handle(self, ctx):
        print("Handling in B -> switching to A")
        ctx._current = ModeA()
        ctx._current.enter(ctx)
if __name__ == "__main__":
    c = Context(ModeA())
    c.request()
    c.request()
    c.request()
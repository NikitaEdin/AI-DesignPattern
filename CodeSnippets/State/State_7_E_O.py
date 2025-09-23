class ModeBase:
    def handle(self, ctx): raise NotImplementedError

class ModeA(ModeBase):
    def handle(self, ctx):
        print("Mode A: handling, switching to B")
        ctx.set_mode(ModeB())

class ModeB(ModeBase):
    def handle(self, ctx):
        print("Mode B: handling, switching to A")
        ctx.set_mode(ModeA())

class Context:
    def __init__(self, mode): self.mode = mode
    def set_mode(self, mode): self.mode = mode
    def request(self): self.mode.handle(self)

if __name__ == "__main__":
    ctx = Context(ModeA())
    ctx.request()
    ctx.request()
    ctx.request()
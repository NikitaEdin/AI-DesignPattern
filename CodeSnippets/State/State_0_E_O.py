import abc
class Mode(abc.ABC):
    @abc.abstractmethod
    def handle(self, m): pass
class ModeA(Mode):
    def handle(self, m):
        print("Mode A handling; switching to B")
        m.switch_mode(ModeB())
class ModeB(Mode):
    def handle(self, m):
        print("Mode B handling; switching to A")
        m.switch_mode(ModeA())
class Machine:
    def __init__(self, initial): self.current = initial
    def switch_mode(self, new): self.current = new
    def request(self): self.current.handle(self)
if __name__ == "__main__":
    m = Machine(ModeA())
    m.request(); m.request(); m.request()
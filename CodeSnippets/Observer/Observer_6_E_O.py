class Subject:
    def __init__(self):
        self._subs = []
        self._state = None
    def register(self, s): self._subs.append(s)
    def unregister(self, s): self._subs.remove(s)
    def set_state(self, v):
        self._state = v
        for s in list(self._subs): s.update(v)

class Printer:
    def __init__(self, name): self.name = name
    def update(self, v): print(f"{self.name} got {v}")

if __name__ == "__main__":
    pub = Subject()
    a = Printer("A"); b = Printer("B")
    pub.register(a); pub.register(b)
    pub.set_state("hello")
    pub.unregister(b)
    pub.set_state("world")
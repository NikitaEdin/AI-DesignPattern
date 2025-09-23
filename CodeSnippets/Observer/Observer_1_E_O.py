class Publisher:
    def __init__(self): self._listeners = []
    def add_listener(self, l): self._listeners.append(l)
    def remove_listener(self, l): self._listeners.remove(l)
    def set_state(self, v):
        self._state = v
        for l in list(self._listeners): l.update(self._state)

class Listener:
    def update(self, v): raise NotImplementedError

class PrintListener(Listener):
    def __init__(self, name): self.name = name
    def update(self, v): print(f"{self.name} received: {v}")

if __name__ == "__main__":
    p = Publisher()
    a = PrintListener("A"); b = PrintListener("B")
    p.add_listener(a); p.add_listener(b)
    p.set_state(1)
    p.remove_listener(b)
    p.set_state(2)
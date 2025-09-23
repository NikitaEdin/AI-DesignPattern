class Publisher:
    def __init__(self): self._subs = []; self._state = None
    def add_subscriber(self, s):
        if s not in self._subs: self._subs.append(s)
    def remove_subscriber(self, s):
        if s in self._subs: self._subs.remove(s)
    def set_state(self, v):
        self._state = v; self._notify()
    def _notify(self):
        for s in list(self._subs): s.update(self._state)

class Subscriber:
    def update(self, v): raise NotImplementedError

class PrintSubscriber(Subscriber):
    def __init__(self, name): self.name = name
    def update(self, v): print(f"{self.name} received: {v}")

if __name__ == "__main__":
    p = Publisher()
    a = PrintSubscriber("A"); b = PrintSubscriber("B")
    p.add_subscriber(a); p.add_subscriber(b)
    p.set_state("first")
    p.remove_subscriber(b)
    p.set_state("second")
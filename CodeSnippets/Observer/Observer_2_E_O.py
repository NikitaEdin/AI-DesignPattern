class Publisher:
    def __init__(self):
        self._subs = []
    def subscribe(self, s): self._subs.append(s)
    def unsubscribe(self, s): self._subs.remove(s)
    def set_state(self, state):
        self._state = state
        for s in list(self._subs): s.receive(self._state)

class Subscriber:
    def __init__(self, name): self.name = name
    def receive(self, data): print(f"{self.name} received: {data}")

if __name__ == "__main__":
    p = Publisher()
    a = Subscriber("A"); b = Subscriber("B")
    p.subscribe(a); p.subscribe(b)
    p.set_state("first")
    p.unsubscribe(a)
    p.set_state("second")
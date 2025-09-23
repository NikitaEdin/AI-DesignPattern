class Publisher:
    def __init__(self): self._subs = []; self._state = None
    def attach(self, s): self._subs.append(s)
    def detach(self, s): self._subs.remove(s)
    def set_state(self, state):
        self._state = state
        for s in list(self._subs): s.receive(state)

class Subscriber:
    def __init__(self, name): self.name = name
    def receive(self, state): print(f"{self.name} received: {state}")

def main():
    p = Publisher()
    a = Subscriber("A"); b = Subscriber("B")
    p.attach(a); p.attach(b)
    p.set_state("first")
    p.detach(b)
    p.set_state("second")

if __name__ == "__main__":
    main()
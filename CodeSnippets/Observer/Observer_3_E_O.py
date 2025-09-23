class Publisher:
    def __init__(self):
        self._subscribers = []
    def register(self, s): self._subscribers.append(s)
    def unregister(self, s): self._subscribers.remove(s)
    def set_state(self, value):
        for s in list(self._subscribers): s.receive(value)

class Listener:
    def __init__(self, name): self.name = name
    def receive(self, value): print(f"{self.name} received {value}")

if __name__ == "__main__":
    pub = Publisher()
    a = Listener("A")
    b = Listener("B")
    pub.register(a)
    pub.register(b)
    pub.set_state("Hello")
    pub.unregister(b)
    pub.set_state("World")
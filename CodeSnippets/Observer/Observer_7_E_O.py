class Publisher:
    def __init__(self):
        self.subs = []; self.state = None
    def subscribe(self, s):
        self.subs.append(s)
    def unsubscribe(self, s):
        self.subs.remove(s)
    def broadcast(self):
        for s in self.subs:
            s.update(self.state)
    def set_state(self, v):
        self.state = v; self.broadcast()

class Subscriber:
    def __init__(self, name):
        self.name = name
    def update(self, v):
        print(f"{self.name} received: {v}")

if __name__ == "__main__":
    p = Publisher()
    a = Subscriber("A"); b = Subscriber("B")
    p.subscribe(a); p.subscribe(b)
    p.set_state(1)
    p.unsubscribe(a)
    p.set_state(2)
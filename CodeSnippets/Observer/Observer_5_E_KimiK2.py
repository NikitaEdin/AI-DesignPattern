class Publisher:
    def __init__(self):
        self._subs = []
    def add(self, sub):
        self._subs.append(sub)
    def remove(self, sub):
        self._subs.remove(sub)
    def notify(self, msg):
        for sub in self._subs:
            sub.update(msg)

class Subscriber:
    def __init__(self, name):
        self.name = name
    def update(self, msg):
        print(f"{self.name} got: {msg}")

if __name__ == "__main__":
    pub = Publisher()
    a = Subscriber("A")
    b = Subscriber("B")
    pub.add(a)
    pub.add(b)
    pub.notify("hello")
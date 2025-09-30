class Publisher:
    def __init__(self):
        self._subs = []
    def attach(self, sub):
        self._subs.append(sub)
    def detach(self, sub):
        self._subs.remove(sub)
    def notify(self, data):
        for sub in self._subs:
            sub.update(data)

class Subscriber:
    def update(self, data):
        pass

class ConcreteSub(Subscriber):
    def __init__(self, name):
        self.name = name
    def update(self, data):
        print(f"{self.name} got: {data}")

if __name__ == "__main__":
    pub = Publisher()
    a = ConcreteSub("A")
    b = ConcreteSub("B")
    pub.attach(a)
    pub.attach(b)
    pub.notify("hello")
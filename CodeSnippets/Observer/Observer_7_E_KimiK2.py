class Publisher:
    def __init__(self):
        self._subscribers = []
    def attach(self, sub):
        self._subscribers.append(sub)
    def detach(self, sub):
        self._subscribers.remove(sub)
    def notify(self, data):
        for sub in self._subscribers:
            sub.update(data)

class Subscriber:
    def update(self, data):
        pass

class ConcreteSubscriber(Subscriber):
    def __init__(self, name):
        self.name = name
    def update(self, data):
        print(f"{self.name} received: {data}")

if __name__ == "__main__":
    pub = Publisher()
    sub1 = ConcreteSubscriber("A")
    sub2 = ConcreteSubscriber("B")
    pub.attach(sub1)
    pub.attach(sub2)
    pub.notify("Hello")
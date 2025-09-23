class Publisher:
    def __init__(self):
        self._subscribers = []
        self._state = None

    def attach(self, subscriber):
        self._subscribers.append(subscriber)

    def detach(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for sub in self._subscribers:
            sub.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()

class Subscriber:
    def __init__(self, name):
        self._name = name

    def update(self, state):
        print(f"{self._name} received update: {state}")

if __name__ == "__main__":
    pub = Publisher()
    sub1 = Subscriber("Alice")
    sub2 = Subscriber("Bob")
    pub.attach(sub1)
    pub.attach(sub2)
    pub.set_state("Hello World")
    pub.set_state("Goodbye")
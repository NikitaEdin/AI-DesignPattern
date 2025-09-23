class Publisher:
    def __init__(self):
        self._subscribers = []
        self._message = ""

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg
        self.notify()

class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received: {message}")

if __name__ == "__main__":
    pub = Publisher()
    sub1 = Subscriber("Alice")
    sub2 = Subscriber("Bob")
    pub.add_subscriber(sub1)
    pub.add_subscriber(sub2)
    pub.message = "Hello World"
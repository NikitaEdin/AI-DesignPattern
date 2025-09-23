class Publisher:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    
    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

class Subscriber:
    def __init__(self, name):
        self.name = name
    
    def update(self, message):
        print(f"{self.name} received: {message}")

if __name__ == "__main__":
    publisher = Publisher()
    
    sub1 = Subscriber("Alice")
    sub2 = Subscriber("Bob")
    
    publisher.subscribe(sub1)
    publisher.subscribe(sub2)
    
    publisher.notify("Hello World!")
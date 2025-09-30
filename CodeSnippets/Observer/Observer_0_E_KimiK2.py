class Publisher:
    def __init__(self):
        self.subscribers = []
    
    def add(self, subscriber):
        self.subscribers.append(subscriber)
    
    def notify(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)

class Listener:
    def update(self, data):
        print("Received:", data)

if __name__ == "__main__":
    pub = Publisher()
    listener = Listener()
    pub.add(listener)
    pub.notify("Hello")
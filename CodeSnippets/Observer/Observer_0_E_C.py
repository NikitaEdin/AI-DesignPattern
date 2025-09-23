class Subject:
    def __init__(self):
        self._listeners = []
    
    def attach(self, listener):
        self._listeners.append(listener)
    
    def notify(self, data):
        for listener in self._listeners:
            listener.update(data)

class Listener:
    def __init__(self, name):
        self.name = name
    
    def update(self, data):
        print(f"{self.name} received: {data}")

class NewsPublisher(Subject):
    def publish_news(self, news):
        self.notify(news)

if __name__ == "__main__":
    publisher = NewsPublisher()
    
    subscriber1 = Listener("Alice")
    subscriber2 = Listener("Bob")
    
    publisher.attach(subscriber1)
    publisher.attach(subscriber2)
    
    publisher.publish_news("Breaking: New Python release!")
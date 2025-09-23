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

if __name__ == "__main__":
    publisher = Subject()
    
    subscriber1 = Listener("App1")
    subscriber2 = Listener("App2")
    
    publisher.attach(subscriber1)
    publisher.attach(subscriber2)
    
    publisher.notify("Hello World")
    publisher.notify("New Update")
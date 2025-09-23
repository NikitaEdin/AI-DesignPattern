class Subject:
    def __init__(self):
        self._listeners = []
    
    def attach(self, listener):
        self._listeners.append(listener)
    
    def notify(self, message):
        for listener in self._listeners:
            listener.update(message)

class Listener:
    def __init__(self, name):
        self.name = name
    
    def update(self, message):
        print(f"{self.name} received: {message}")

if __name__ == "__main__":
    publisher = Subject()
    
    subscriber1 = Listener("User1")
    subscriber2 = Listener("User2")
    
    publisher.attach(subscriber1)
    publisher.attach(subscriber2)
    
    publisher.notify("Hello World!")
    publisher.notify("Pattern Demo Complete")
class Subject:
    def __init__(self):
        self._listeners = []
        self._state = None
    
    def attach(self, listener):
        self._listeners.append(listener)
    
    def detach(self, listener):
        self._listeners.remove(listener)
    
    def notify(self):
        for listener in self._listeners:
            listener.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class Listener:
    def __init__(self, name):
        self.name = name
    
    def update(self, state):
        print(f"{self.name} received: {state}")

if __name__ == "__main__":
    subject = Subject()
    listener1 = Listener("Listener1")
    listener2 = Listener("Listener2")
    
    subject.attach(listener1)
    subject.attach(listener2)
    subject.set_state("Hello World")
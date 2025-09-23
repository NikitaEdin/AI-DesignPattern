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
            listener.update(self)
    
    def set_state(self, state):
        self._state = state
        self.notify()
    
    def get_state(self):
        return self._state

class Listener:
    def update(self, subject):
        print(f"State changed to: {subject.get_state()}")

if __name__ == "__main__":
    subject = Subject()
    listener1 = Listener()
    listener2 = Listener()
    
    subject.attach(listener1)
    subject.attach(listener2)
    
    subject.set_state("New State")
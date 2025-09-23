class Subject:
    def __init__(self):
        self._listeners = []
    def add_listener(self, listener):
        self._listeners.append(listener)
    def remove_listener(self, listener):
        self._listeners.remove(listener)
    def notify_listeners(self, message):
        for l in list(self._listeners):
            l.update(message)

class ListenerBase:
    def update(self, message):
        raise NotImplementedError

class PrintListener(ListenerBase):
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print(f"{self.name} received: {message}")

if __name__ == "__main__":
    s = Subject()
    a = PrintListener("A")
    b = PrintListener("B")
    s.add_listener(a)
    s.add_listener(b)
    s.notify_listeners("First update")
    s.remove_listener(b)
    s.notify_listeners("Second update")
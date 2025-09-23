class Subject:
    def __init__(self):
        self._observers = set()

    def register(self, observer):
        if observer not in self._observers:
            self._observers.add(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

class Observer:
    def __init__(self, subject):
        self.subject = subject
        self.subject.register(self)

    def update(self, data):
        print(f"Received data: {data}")

if __name__ == "__main__":
    # Create a subject and two observers
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)

    # Notify the subject with some data
    subject.notify("Hello, world!")

    # Unregister one of the observers
    subject.unregister(observer1)

    # Notify the subject again with different data
    subject.notify("Goodbye, world!")
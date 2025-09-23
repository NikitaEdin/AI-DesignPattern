```python
class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify_all(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.attach(self)

    def update(self, message):
        print("Update:", message)

if __name__ == "__main__":
    # Create a Subject and attach two Observers to it
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)

    # Notify all attached observers of a message
    subject.notify_all("Hello, world!")
  ```
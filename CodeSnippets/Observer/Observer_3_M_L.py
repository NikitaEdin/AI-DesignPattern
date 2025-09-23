class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.attach(self)

    def update(self, data):
        print(f"Received update from {self._subject}: {data}")

if __name__ == "__main__":
    subject = Subject()
    observer_1 = Observer(subject)
    observer_2 = Observer(subject)

    subject.notify("Hello, world!")
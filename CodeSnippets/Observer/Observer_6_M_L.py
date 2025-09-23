class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)

class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.register(self)

    def update(self, *args, **kwargs):
        pass

class ConcreteObserver(Observer):
    def update(self, *args, **kwargs):
        print("Received update:", args, kwargs)

if __name__ == "__main__":
    subject = Subject()
    observer1 = ConcreteObserver(subject)
    observer2 = ConcreteObserver(subject)

    subject.notify_all("Hello", world="Python")
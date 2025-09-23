class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)

class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.attach(self)

    def update(self, *args, **kwargs):
        print("Update called with args {}, kwargs {}".format(args, kwargs))

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)
    subject.notify_all(42, foo="bar")
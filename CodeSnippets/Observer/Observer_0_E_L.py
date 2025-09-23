import logging

class Subject:
    def __init__(self):
        self._observers = set()

    def register(self, observer):
        if observer not in self._observers:
            self._observers.add(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, *args):
        for observer in self._observers:
            observer(*args)

class Observer:
    def __init__(self, subject):
        self.subject = subject
        subject.register(self)

    def update(self, *args):
        print("Update called")

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)
    subject.notify_all("Hello", "World")
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.attach(self)

    def update(self):
        pass # implement the logic to handle the update here

def main():
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)

    subject.notify()
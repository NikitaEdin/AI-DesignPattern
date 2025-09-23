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
        subject.attach(self)

    def update(self, data):
        print("Observer received data:", data)

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)
    subject.notify("Hello World!")
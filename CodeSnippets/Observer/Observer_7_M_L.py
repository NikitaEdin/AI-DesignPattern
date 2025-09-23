class Subject:
    def __init__(self) -> None:
        self._observers = set()

    def register_observer(self, observer: Observer) -> None:
        if not isinstance(observer, Observer):
            raise ValueError("Expected an instance of the Observer class")
        self._observers.add(observer)

    def unregister_observer(self, observer: Observer) -> None:
        if not isinstance(observer, Observer):
            raise ValueError("Expected an instance of the Observer class")
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update()

class Observer:
    def __init__(self, subject: Subject) -> None:
        if not isinstance(subject, Subject):
            raise ValueError("Expected an instance of the Subject class")
        self._subject = subject
        self._subject.register_observer(self)

    def update(self) -> None:
        print(f"{self.__class__.__name__} received a notification from {self._subject}")

class ConcreteObserver1(Observer):
    pass

class ConcreteObserver2(Observer):
    pass

if __name__ == "__main__":
    subject = Subject()
    observer1 = ConcreteObserver1(subject)
    observer2 = ConcreteObserver2(subject)

    subject.notify_observers()
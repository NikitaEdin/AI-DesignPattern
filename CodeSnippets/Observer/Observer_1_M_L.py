import typing

class Subject:
    def __init__(self) -> None:
        self._observers = set()

    def attach_observer(self, observer: typing.Any) -> None:
        if observer not in self._observers:
            self._observers.add(observer)

    def detach_observer(self, observer: typing.Any) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, *args) -> None:
        for observer in self._observers:
            observer.update(*args)

class Observer:
    def __init__(self, subject: Subject) -> None:
        self._subject = subject
        self._subject.attach_observer(self)

    def update(self, *args) -> None:
        raise NotImplementedError()

class ConcreteObserver(Observer):
    def __init__(self, subject: Subject) -> None:
        super().__init__(subject)

    def update(self, arg1: str, arg2: int) -> None:
        print("Received update from the subject.")
        print(f"Arg 1: {arg1}")
        print(f"Arg 2: {arg2}")

if __name__ == "__main__":
    subject = Subject()
    observer1 = ConcreteObserver(subject)
    observer2 = ConcreteObserver(subject)
    subject.notify_observers("hello", 42)
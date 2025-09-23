```python
import abc

class Subject(abc.ABC):
    def __init__(self):
        self._observers = []

    def attach_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass

def main():
    subject = Subject()
    observer1 = Observer()
    observer2 = Observer()

    subject.attach_observer(observer1)
    subject.attach_observer(observer2)

    # simulate state change
    print("State changed!")
    subject.notify_observers()

if __name__ == "__main__":
    main()
  ```
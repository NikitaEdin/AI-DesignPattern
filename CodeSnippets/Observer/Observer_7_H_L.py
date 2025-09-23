class Observable:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_all(self, *args):
        for observer in self._observers:
            observer(*args)

class Observer:
    def __init__(self, observable):
        self._observable = observable
        self._observable.attach(self)
    
    def detach(self):
        self._observable.detach(self)
    
    def update(self, *args):
        pass  # override this method to handle updates

class ConcreteObserver(Observer):
    def update(self, value):
        print(f"Received update: {value}")

# Example usage
if __name__ == "__main__":
    observable = Observable()
    observer1 = ConcreteObserver(observable)
    observer2 = ConcreteObserver(observable)
    observable.notify_all("Hello")
    observable.detach(observer1)
    observable.notify_all("World")
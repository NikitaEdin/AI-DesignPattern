class Subject:
    def __init__(self):
        self._observers = set()
    
    def attach(self, observer):
        if not isinstance(observer, Observer):
            raise ValueError("The observer must be an instance of the Observer class")
        
        self._observers.add(observer)
    
    def detach(self, observer):
        if not isinstance(observer, Observer):
            raise ValueError("The observer must be an instance of the Observer class")
        
        self._observers.remove(observer)
    
    def notify_all(self):
        for observer in self._observers:
            observer.update()

class Observer:
    def __init__(self, subject):
        self._subject = subject
    
    def update(self):
        print("Update")

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)
    subject.attach(observer1)
    subject.attach(observer2)
    subject.notify_all()
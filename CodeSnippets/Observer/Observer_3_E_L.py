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
    def update(self):
        pass

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer()
    observer2 = Observer()
    
    subject.attach(observer1)
    subject.attach(observer2)
    
    subject.notify()
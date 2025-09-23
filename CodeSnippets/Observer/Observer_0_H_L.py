class Subject:
    def __init__(self):
        self.observers = []
    
    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self, data):
        for observer in self.observers:
            observer.update(data)

class Observer:
    def __init__(self, subject):
        self.subject = subject
        self.subject.register(self)
    
    def update(self, data):
        print("Observer received data:", data)
    
    def __del__(self):
        self.subject.unregister(self)

if __name__ == "__main__":
    subject = Subject()
    observer1 = Observer(subject)
    observer2 = Observer(subject)
    subject.notify("Hello, World!")
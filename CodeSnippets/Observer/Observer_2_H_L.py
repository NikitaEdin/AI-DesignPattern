# An implementation of the Observer pattern in Python
class Subject:
    def __init__(self):
        self._observers = []
    
    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_all(self):
        for observer in self._observers:
            observer.update()
            
class Observer:
    def __init__(self, subject):
        self._subject = subject
        self._subject.register(self)
    
    def update(self):
        # Implement the update method for each observer
        pass
        
# Example usage of the Observer pattern
if __name__ == "__main__":
    # Create a subject and an observer
    subject = Subject()
    observer = Observer(subject)
    
    # Register another observer
    observer2 = Observer(subject)
    
    # Update the subject, which will notify both observers
    subject.notify_all()
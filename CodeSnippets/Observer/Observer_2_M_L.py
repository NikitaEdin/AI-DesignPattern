class Subject:
    def __init__(self):
        self._observers = set()
    
    def attach(self, observer):
        self._observers.add(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify_all(self, *args):
        for observer in self._observers:
            observer(*args)
            
class Observer:
    def __init__(self, subject, callback):
        self._subject = subject
        self._callback = callback
        
    def update(self):
        self._subject.notify_all(self._callback)
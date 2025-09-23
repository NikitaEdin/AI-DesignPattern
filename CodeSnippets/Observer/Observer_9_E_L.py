class NotificationCenter:
    def __init__(self):
        self.observers = set()
    
    def register(self, observer):
        self.observers.add(observer)
    
    def unregister(self, observer):
        self.observers.remove(observer)
    
    def notify(self, notification):
        for observer in self.observers:
            observer.update(notification)

class User:
    def __init__(self, name):
        self.name = name
    
    def update(self, notification):
        print(f"User {self.name} received notification: {notification}")

if __name__ == "__main__":
    center = NotificationCenter()
    user1 = User("Alice")
    user2 = User("Bob")
    
    center.register(user1)
    center.register(user2)
    
    center.notify("New message from John")
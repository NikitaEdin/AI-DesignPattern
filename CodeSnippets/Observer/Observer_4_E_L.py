class NotificationCenter:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_all(self, message):
        for observer in self.observers:
            observer.update(message)

class User:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received message: {message}")

if __name__ == "__main__":
    notification_center = NotificationCenter()

    user1 = User("Alice")
    user2 = User("Bob")

    notification_center.add_observer(user1)
    notification_center.add_observer(user2)

    notification_center.notify_all("Hello, world!")
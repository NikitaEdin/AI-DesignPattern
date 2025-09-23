class User:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print(f"{self.name} received notification: {message}")

class NotificationCenter:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def notify_all(self, message):
        for observer in self.observers:
            observer.notify(message)

if __name__ == "__main__":
    notification_center = NotificationCenter()

    user1 = User("Alice")
    user2 = User("Bob")

    notification_center.register(user1)
    notification_center.register(user2)

    message = "New task added"
    notification_center.notify_all(message)
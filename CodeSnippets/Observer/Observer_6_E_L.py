class NotificationCenter:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, message):
        for observer in self._observers:
            observer.update(message)

class User:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"User {self.name} received message: {message}")

if __name__ == "__main__":
    # Create a notification center and two users
    notification_center = NotificationCenter()
    user1 = User("Alice")
    user2 = User("Bob")

    # Subscribe both users to the notification center
    notification_center.subscribe(user1)
    notification_center.subscribe(user2)

    # Send a message from the notification center
    notification_center.notify_all("Hello, world!")
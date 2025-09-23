class NotificationCenter:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class User:
    def __init__(self, name):
        self.name = name

    def update(self, event):
        print(f"{self.name} received an update: {event}")

if __name__ == "__main__":
    # Create a notification center
    nc = NotificationCenter()

    # Register two users to receive notifications
    user1 = User("Alice")
    user2 = User("Bob")
    nc.register(user1)
    nc.register(user2)

    # Notify the notification center of an event
    nc.notify("New message from Jane")

    # Unregister one of the users
    nc.unregister(user1)

    # Notify again, and only the other user should receive an update
    nc.notify("New message from John")
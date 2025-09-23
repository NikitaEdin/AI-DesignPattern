class User:
    def __init__(self, name: str):
        self.name = name
        self.notifications = []

    def add_notification(self, notification: dict):
        self.notifications.append(notification)

    def get_notifications(self) -> list[dict]:
        return self.notifications

class NotificationCenter:
    def __init__(self):
        self.users = {}

    def register_user(self, user: User):
        self.users[user.name] = user

    def notify_all(self, notification: dict):
        for user in self.users.values():
            user.add_notification(notification)

if __name__ == "__main__":
    notification_center = NotificationCenter()

    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Charlie")

    notification_center.register_user(user1)
    notification_center.register_user(user2)
    notification_center.register_user(user3)

    notification_center.notify_all({"message": "Hello, world!"})

    print(user1.get_notifications())
    print(user2.get_notifications())
    print(user3.get_notifications())
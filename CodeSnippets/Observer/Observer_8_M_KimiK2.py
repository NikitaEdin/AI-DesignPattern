class Publisher:
    def __init__(self):
        self._followers = []

    def register(self, follower):
        if follower not in self._followers:
            self._followers.append(follower)
        else:
            raise ValueError("Already registered")

    def unregister(self, follower):
        try:
            self._followers.remove(follower)
        except ValueError:
            raise ValueError("Not registered")

    def notify_all(self, data):
        for follower in self._followers:
            follower.update(data)


class ConcretePublisher(Publisher):
    def __init__(self):
        super().__init__()
        self._state = None

    def set_state(self, state):
        self._state = state
        self.notify_all(state)


class Subscriber:
    def update(self, data):
        raise NotImplementedError


class EmailSubscriber(Subscriber):
    def __init__(self, name):
        self._name = name

    def update(self, data):
        print(f"[{self._name}] Email sent with data: {data}")


class SMSSubscriber(Subscriber):
    def __init__(self, name):
        self._name = name

    def update(self, data):
        print(f"[{self._name}] SMS sent with data: {data}")


if __name__ == "__main__":
    pub = ConcretePublisher()
    email1 = EmailSubscriber("Alice")
    sms1 = SMSSubscriber("Bob")
    pub.register(email1)
    pub.register(sms1)
    pub.set_state("New message")
    pub.unregister(email1)
    pub.set_state("Another update")
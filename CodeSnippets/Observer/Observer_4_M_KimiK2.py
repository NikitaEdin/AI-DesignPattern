class Receiver:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received: {message}")


class Broadcaster:
    def __init__(self):
        self._receivers = []

    def attach(self, receiver):
        if receiver not in self._receivers:
            self._receivers.append(receiver)

    def detach(self, receiver):
        try:
            self._receivers.remove(receiver)
        except ValueError:
            pass

    def notify(self, message):
        for receiver in self._receivers:
            receiver.update(message)

    def broadcast(self, message):
        self.notify(message)


if __name__ == "__main__":
    broadcaster = Broadcaster()
    alice = Receiver("Alice")
    bob = Receiver("Bob")
    broadcaster.attach(alice)
    broadcaster.attach(bob)
    broadcaster.broadcast("Hello all!")
    broadcaster.detach(bob)
    broadcaster.broadcast("Bob should not see this.")
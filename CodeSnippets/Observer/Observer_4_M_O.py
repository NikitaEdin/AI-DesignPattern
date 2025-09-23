class Publisher:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber, condition=None):
        notify = getattr(subscriber, "notify", None)
        if not callable(notify):
            raise TypeError("Subscriber must implement a callable 'notify(event)' method")
        if condition is not None and not callable(condition):
            raise TypeError("condition must be callable or None")
        self._subscribers.append((subscriber, condition))

    def unsubscribe(self, subscriber):
        self._subscribers = [(s, c) for (s, c) in self._subscribers if s is not subscriber]

    def broadcast(self, event):
        for subscriber, condition in list(self._subscribers):
            try:
                if condition is None or condition(event):
                    subscriber.notify(event)
            except Exception as exc:
                import sys
                print(f"Error delivering event to {subscriber}: {exc}", file=sys.stderr)


class PrintSubscriber:
    def __init__(self, name):
        self.name = name

    def notify(self, event):
        print(f"[{self.name}] received: {event}")


class FaultySubscriber:
    def __init__(self, name):
        self.name = name

    def notify(self, event):
        raise RuntimeError(f"{self.name} failed while handling {event}")


if __name__ == "__main__":
    publisher = Publisher()
    alice = PrintSubscriber("Alice")
    bob = PrintSubscriber("Bob")
    charlie = FaultySubscriber("Charlie")

    publisher.subscribe(alice)
    publisher.subscribe(bob, condition=lambda e: isinstance(e, dict) and e.get("type") == "update")
    publisher.subscribe(charlie)

    events = [
        "simple_message",
        {"type": "update", "data": 42},
        {"type": "other", "data": "ignore"},
    ]

    for ev in events:
        print("Publishing:", ev)
        publisher.broadcast(ev)

    publisher.unsubscribe(alice)
    print("After unsubscribing Alice")
    publisher.broadcast("final_message")
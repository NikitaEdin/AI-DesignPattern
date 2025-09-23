class Publisher:
    def __init__(self):
        self._subscribers = set()
    def attach(self, subscriber):
        if not callable(getattr(subscriber, "update", None)):
            raise TypeError("Subscriber must implement update(event)")
        self._subscribers.add(subscriber)
    def detach(self, subscriber):
        self._subscribers.discard(subscriber)
    def publish(self, event):
        errors = []
        for s in list(self._subscribers):
            try:
                s.update(event)
            except Exception as exc:
                errors.append((s, exc))
        for s, exc in errors:
            print(f"Error notifying {type(s).__name__}: {exc}")

class ConsoleClient:
    def __init__(self, name):
        self.name = name
    def update(self, event):
        print(f"{self.name} received: {event}")

class FaultyClient:
    def update(self, event):
        raise RuntimeError("processing failed")

class FilterClient:
    def __init__(self, min_level):
        self.min_level = min_level
    def update(self, event):
        if isinstance(event, dict) and event.get("level", 0) >= self.min_level:
            print(f"Filtered received: {event}")

if __name__ == "__main__":
    pub = Publisher()
    a = ConsoleClient("A"); b = ConsoleClient("B")
    f = FaultyClient(); fl = FilterClient(5)
    for s in (a, b, f, fl): pub.attach(s)
    pub.publish({"msg": "low importance", "level": 2})
    pub.publish({"msg": "high importance", "level": 7})
    pub.detach(b); pub.publish({"msg": "post detach", "level": 10})
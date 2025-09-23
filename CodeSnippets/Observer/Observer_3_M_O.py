class Publisher:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, handler, filter_fn=None):
        if not callable(getattr(handler, "update", None)):
            raise TypeError("handler must implement update(event)")
        if filter_fn is not None and not callable(filter_fn):
            raise TypeError("filter_fn must be callable")
        self._subscribers.append((handler, filter_fn))

    def unsubscribe(self, handler):
        before = len(self._subscribers)
        self._subscribers = [(h, f) for (h, f) in self._subscribers if h is not handler]
        if len(self._subscribers) == before:
            raise ValueError("handler not found")

    def publish(self, event):
        errors = []
        for handler, filter_fn in list(self._subscribers):
            try:
                if filter_fn and not filter_fn(event):
                    continue
                handler.update(event)
            except Exception as exc:
                errors.append((handler, exc))
        if errors:
            summaries = "; ".join(f"{type(h).__name__}:{type(e).__name__}" for h, e in errors)
            raise RuntimeError(f"publish encountered errors: {summaries}")


class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, event):
        print(f"{self.name} received event: {event}")


class FaultySubscriber:
    def update(self, event):
        raise RuntimeError("simulated failure")


if __name__ == "__main__":
    p = Publisher()
    s1 = Subscriber("Alpha")
    s2 = Subscriber("Beta")
    f = FaultySubscriber()

    p.subscribe(s1)
    p.subscribe(s2, filter_fn=lambda e: e.get("level", 0) >= 5)
    p.subscribe(f)

    events = [
        {"message": "low", "level": 1},
        {"message": "high", "level": 7},
    ]

    for ev in events:
        try:
            p.publish(ev)
        except RuntimeError as err:
            print("Publish error:", err)

    try:
        p.unsubscribe(s1)
        p.unsubscribe(s1)
    except ValueError as err:
        print("Unsubscribe error:", err)
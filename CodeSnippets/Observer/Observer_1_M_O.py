import abc
from typing import Callable, Any, List, Dict

class SubscriberBase(abc.ABC):
    @abc.abstractmethod
    def notify(self, source: Any, event: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._listeners: List[Dict] = []

    def add_listener(self, subscriber: SubscriberBase, predicate: Callable[[Any], bool] = None, once: bool = False, priority: int = 0):
        if not callable(getattr(subscriber, "notify", None)):
            raise TypeError("Subscriber must implement notify(source, event)")
        if any(entry["subscriber"] is subscriber for entry in self._listeners):
            raise ValueError("Subscriber already registered")
        entry = {"subscriber": subscriber, "predicate": predicate or (lambda e: True), "once": once, "priority": priority}
        self._listeners.append(entry)
        self._listeners.sort(key=lambda x: -x["priority"])

    def remove_listener(self, subscriber: SubscriberBase):
        before = len(self._listeners)
        self._listeners = [e for e in self._listeners if e["subscriber"] is not subscriber]
        if len(self._listeners) == before:
            raise ValueError("Subscriber not found")

    def emit(self, event: Any):
        to_remove = []
        for entry in list(self._listeners):
            try:
                if entry["predicate"](event):
                    entry["subscriber"].notify(self, event)
                    if entry["once"]:
                        to_remove.append(entry["subscriber"])
            except Exception as exc:
                # basic error handling keeps other listeners running
                try:
                    entry["subscriber"].notify(self, {"error": str(exc), "original": event})
                except Exception:
                    pass
        for sub in to_remove:
            self._listeners = [e for e in self._listeners if e["subscriber"] is not sub]

class PrintSubscriber(SubscriberBase):
    def __init__(self, name: str):
        self.name = name
    def notify(self, source, event):
        print(f"{self.name} received: {event}")

class ThresholdSubscriber(SubscriberBase):
    def __init__(self, threshold: float):
        self.threshold = threshold
    def notify(self, source, event):
        if isinstance(event, (int, float)) and event > self.threshold:
            print(f"Threshold hit: {event} > {self.threshold}")

if __name__ == "__main__":
    publisher = Publisher()
    p1 = PrintSubscriber("Logger")
    p2 = PrintSubscriber("OneTime")
    t1 = ThresholdSubscriber(50)

    publisher.add_listener(p1, priority=1)
    publisher.add_listener(p2, once=True)
    publisher.add_listener(t1, predicate=lambda v: isinstance(v, (int, float)))

    for value in [10, 60, 30, 80]:
        print(f"Emitting: {value}")
        publisher.emit(value)
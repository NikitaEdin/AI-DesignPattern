from typing import Callable, Any

class SubjectManager:
    def __init__(self):
        self._listeners = []
        self._state = None

    def register(self, callback: Callable[[Any], None], predicate: Callable[[Any], bool] = lambda _: True):
        if not callable(callback) or not callable(predicate):
            raise TypeError("callback and predicate must be callable")
        self._listeners.append((callback, predicate))

    def unregister(self, callback: Callable[[Any], None]):
        original = len(self._listeners)
        self._listeners = [(cb, pr) for cb, pr in self._listeners if cb != callback]
        if len(self._listeners) == original:
            raise ValueError("callback not registered")

    def update_state(self, new_state: Any):
        self._state = new_state
        self._notify_all(new_state)

    def _notify_all(self, state: Any):
        for callback, predicate in list(self._listeners):
            try:
                if predicate(state):
                    callback(state)
            except Exception as exc:
                print(f"Listener error: {exc}")

class SubscriberBase:
    def __init__(self, name: str):
        self.name = name

    def handle(self, state: Any):
        raise NotImplementedError

class PrintSubscriber(SubscriberBase):
    def handle(self, state: Any):
        print(f"{self.name} received state: {state}")

class ThresholdSubscriber(SubscriberBase):
    def __init__(self, name: str, threshold: float):
        super().__init__(name)
        self.threshold = threshold

    def handle(self, state: Any):
        if not isinstance(state, (int, float)):
            raise TypeError("state must be numeric for threshold check")
        print(f"{self.name} threshold {self.threshold} triggered by {state}")

class FaultySubscriber(SubscriberBase):
    def handle(self, state: Any):
        raise RuntimeError("simulated failure")

if __name__ == "__main__":
    manager = SubjectManager()
    p1 = PrintSubscriber("PrinterA")
    p2 = ThresholdSubscriber("ThreshB", 10)
    faulty = FaultySubscriber("Broken")

    manager.register(p1.handle)
    manager.register(p2.handle, predicate=lambda s: isinstance(s, (int, float)) and s > 10)
    manager.register(faulty.handle)

    manager.update_state("startup")
    manager.update_state(5)
    manager.update_state(15)

    try:
        manager.unregister(lambda x: x)  # will raise
    except ValueError:
        pass

    manager.unregister(faulty.handle)
    manager.update_state(20)
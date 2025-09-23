from typing import Callable, Any, Optional, List, Tuple

class Publisher:
    def __init__(self) -> None:
        self._subscribers: List[Tuple[object, Optional[Callable[[Any], bool]]]] = []

    def subscribe(self, listener: object, condition: Optional[Callable[[Any], bool]] = None) -> None:
        if not hasattr(listener, "notify") or not callable(getattr(listener, "notify")):
            raise TypeError("Listener must provide a callable 'notify' method")
        if any(s is listener for s, _ in self._subscribers):
            raise ValueError("Listener already registered")
        self._subscribers.append((listener, condition))

    def unsubscribe(self, listener: object) -> None:
        for i, (s, _) in enumerate(self._subscribers):
            if s is listener:
                del self._subscribers[i]
                return
        raise ValueError("Listener not found")

    def publish(self, payload: Any) -> None:
        for listener, condition in list(self._subscribers):
            try:
                if condition is None or condition(payload):
                    listener.notify(payload)
            except Exception:
                try:
                    self.unsubscribe(listener)
                except ValueError:
                    pass

class LoggerSubscriber:
    def __init__(self, name: str) -> None:
        self.name = name
    def notify(self, message: Any) -> None:
        print(f"[LOG:{self.name}] {message}")

class EmailSubscriber:
    def __init__(self, address: str) -> None:
        self.address = address
    def notify(self, message: Any) -> None:
        print(f"Sending email to {self.address}: {message}")

class FailingSubscriber:
    def notify(self, message: Any) -> None:
        raise RuntimeError("simulated failure")

if __name__ == "__main__":
    hub = Publisher()
    logger = LoggerSubscriber("main")
    email = EmailSubscriber("team@example.com")
    failing = FailingSubscriber()

    hub.subscribe(logger)
    hub.subscribe(email, condition=lambda m: "urgent" in str(m).lower())
    hub.subscribe(failing)

    hub.publish("Regular update")
    hub.publish("URGENT: action required")

    try:
        hub.subscribe(object())  # should raise
    except TypeError as exc:
        print("Subscribe error:", exc)

    hub.publish("Final notice")
    try:
        hub.unsubscribe(failing)
    except ValueError as exc:
        print("Unsubscribe error:", exc)
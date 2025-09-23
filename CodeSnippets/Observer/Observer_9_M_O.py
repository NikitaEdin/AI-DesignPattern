import logging
from typing import Callable, Optional, List, Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

class Publisher:
    def __init__(self) -> None:
        self._subscribers: List[Tuple[Callable[[dict], None], Optional[Callable[[dict], bool]]]] = []

    def subscribe(self, callback: Callable[[dict], None], condition: Optional[Callable[[dict], bool]] = None) -> None:
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._subscribers.append((callback, condition))

    def unsubscribe(self, callback: Callable[[dict], None]) -> None:
        self._subscribers = [(cb, cond) for (cb, cond) in self._subscribers if cb != callback]

    def broadcast(self, event: dict) -> None:
        for callback, condition in list(self._subscribers):
            try:
                if condition is None or condition(event):
                    callback(event)
            except Exception as exc:
                logging.exception("Error delivering event: %s", exc)

class Printer:
    def __init__(self, name: str) -> None:
        self.name = name

    def handle(self, event: dict) -> None:
        logging.info("%s received: %s", self.name, event)

class FaultyHandler:
    def handle(self, event: dict) -> None:
        raise RuntimeError("simulated failure")

if __name__ == "__main__":
    hub = Publisher()
    p1 = Printer("ListenerA")
    p2 = Printer("ListenerB")
    faulty = FaultyHandler()

    hub.subscribe(p1.handle)
    hub.subscribe(p2.handle, condition=lambda e: e.get("priority") == "high")
    hub.subscribe(faulty.handle)

    hub.broadcast({"message": "hello", "priority": "low"})
    hub.broadcast({"message": "urgent update", "priority": "high"})

    hub.unsubscribe(faulty.handle)
    hub.broadcast({"message": "final", "priority": "high"})
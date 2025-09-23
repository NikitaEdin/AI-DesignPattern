import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventHub:
    def __init__(self):
        self._lock = threading.Lock()
        self._subscriptions = []  # list of dicts: {'id', 'subscriber', 'filter', 'once'}
        self._next_id = 1

    def subscribe(self, subscriber, filter_fn=None, once=False):
        if not hasattr(subscriber, "receive") or not callable(subscriber.receive):
            raise TypeError("subscriber must implement a callable receive(event) method")
        with self._lock:
            sid = self._next_id
            self._next_id += 1
            self._subscriptions.append(
                {"id": sid, "subscriber": subscriber, "filter": filter_fn, "once": bool(once)}
            )
            return sid

    def unsubscribe(self, subscription_id=None, subscriber=None):
        with self._lock:
            if subscription_id is not None:
                self._subscriptions = [s for s in self._subscriptions if s["id"] != subscription_id]
            elif subscriber is not None:
                self._subscriptions = [s for s in self._subscriptions if s["subscriber"] is not subscriber]
            else:
                raise ValueError("provide subscription_id or subscriber to unsubscribe")

    def publish(self, event):
        with self._lock:
            snapshot = list(self._subscriptions)
        remove_ids = []
        for s in snapshot:
            # filter evaluation
            try:
                if s["filter"] is not None and not s["filter"](event):
                    continue
            except Exception:
                logger.exception("Filter function raised for subscriber %r", s["subscriber"])
                continue
            # attempt delivery; count as attempted even if receive raises
            attempted = True
            try:
                s["subscriber"].receive(event)
            except Exception:
                logger.exception("Error delivering event to %r", s["subscriber"])
            if s["once"] and attempted:
                remove_ids.append(s["id"])
        if remove_ids:
            with self._lock:
                ids = set(remove_ids)
                self._subscriptions = [s for s in self._subscriptions if s["id"] not in ids]


# Example usage
class PrintClient:
    def __init__(self, name):
        self.name = name

    def receive(self, event):
        print(f"{self.name} received: {event}")


class ErrorClient:
    def receive(self, event):
        raise RuntimeError("delivery failed")


if __name__ == "__main__":
    hub = EventHub()
    a = PrintClient("A")
    b = PrintClient("B")
    err = ErrorClient()

    # multiple subscriptions for same object allowed, with different filters/once flags
    hub.subscribe(a)  # persistent
    hub.subscribe(a, filter_fn=lambda e: "x" in str(e), once=True)  # one-time, conditional
    sid_b = hub.subscribe(b, once=True)
    hub.subscribe(err)

    hub.publish("first event")
    hub.publish("event with x")
    hub.publish("another event")
    # unsubscribe specific
    hub.unsubscribe(subscription_id=sid_b)
    hub.publish("final x event")
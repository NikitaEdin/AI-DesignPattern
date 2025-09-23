class Publisher:
    def __init__(self):
        self._subs = []
    def subscribe(self, subscriber, filter_func=None):
        if not hasattr(subscriber, "notify"):
            raise TypeError("Subscriber must implement notify(message, event_type)")
        self._subs.append((subscriber, filter_func))
    def unsubscribe(self, subscriber):
        self._subs = [(s,f) for s,f in self._subs if s is not subscriber]
    def publish(self, message, event_type=None):
        errors = []
        for s, f in list(self._subs):
            try:
                if f is None or f(event_type, message):
                    s.notify(message, event_type)
            except Exception as e:
                errors.append((s, e))
        return errors

class Subscriber:
    def __init__(self, name, handler=None):
        self.name = name
        self._handler = handler or (lambda m, e: print(f"{self.name} received [{e}]: {m}"))
    def notify(self, message, event_type):
        self._handler(message, event_type)

if __name__ == "__main__":
    pub = Publisher()
    pub.subscribe(Subscriber("Logger"))
    pub.subscribe(
        Subscriber("ErrorsOnly", handler=lambda m, e: print("ERROR:", m) if e == "error" else None),
        filter_func=lambda et, m: et == "error"
    )
    pub.subscribe(
        Subscriber("OddNumbers", handler=lambda m, e: print("Odd number:", m) if isinstance(m, int) and m % 2 else None),
        filter_func=lambda et, m: isinstance(m, int) and m % 2 == 1
    )
    pub.publish("Welcome", event_type="info")
    pub.publish("Failure", event_type="error")
    pub.publish(3, event_type="number")
    pub.publish(4, event_type="number")
    broken = Subscriber("Broken", handler=lambda m, e: (_ for _ in ()).throw(RuntimeError("handler failed")))
    pub.subscribe(broken)
    errs = pub.publish("Test", event_type="test")
    if errs:
        print("Subscriber errors:", [(s.name, str(ex)) for s, ex in errs])
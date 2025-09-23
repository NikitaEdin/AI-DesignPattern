import weakref

class StockPricePublisher:
    def __init__(self):
        self._price = 0.0
        self._listeners = []

    def add_listener(self, listener):
        if any(ref() == listener for ref in self._listeners if ref() is not None):
            return
        self._listeners.append(weakref.ref(listener))

    def remove_listener(self, listener):
        for i, ref in enumerate(self._listeners):
            if ref() == listener:
                del self._listeners[i]
                return

    def set_price(self, price):
        self._price = price
        self._notify_listeners()

    def _notify_listeners(self):
        dead_refs = []
        for i, ref in enumerate(self._listeners):
            listener = ref()
            if listener is None:
                dead_refs.append(i)
            else:
                try:
                    listener.update_price(self._price)
                except Exception:
                    pass
        for i in reversed(dead_refs):
            del self._listeners[i]

class PriceDisplay:
    def __init__(self, name):
        self.name = name

    def update_price(self, price):
        print(f"{self.name} updated with price: {price:.2f}")

class MobileAlert:
    def __init__(self, user):
        self.user = user

    def update_price(self, price):
        if price > 100.0:
            print(f"Alert for {self.user}: Price exceeded 100 at {price:.2f}!")

if __name__ == "__main__":
    publisher = StockPricePublisher()
    display1 = PriceDisplay("Main Screen")
    display2 = PriceDisplay("Backup Screen")
    alert = MobileAlert("John Doe")

    publisher.add_listener(display1)
    publisher.add_listener(display2)
    publisher.add_listener(alert)

    publisher.set_price(95.0)
    publisher.set_price(105.0)
    publisher.set_price(120.0)

    publisher.remove_listener(display2)
    publisher.set_price(130.0)

    # Simulate a dead listener by overwriting
    display1 = None  # But since weakref, it will be cleaned on next notify
    publisher.set_price(140.0)
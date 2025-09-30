class Publisher:
    def __init__(self):
        self._subscribers = set()

    def follow(self, subscriber):
        self._subscribers.add(subscriber)

    def unfollow(self, subscriber):
        self._subscribers.discard(subscriber)

    def notify(self, data):
        for subscriber in list(self._subscribers):
            try:
                subscriber.update(data)
            except Exception:
                self.unfollow(subscriber)

class Subscriber:
    def update(self, data):
        raise NotImplementedError

class StockMonitor(Publisher):
    def __init__(self):
        super().__init__()
        self._price = 0.0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        self.notify(value)

class StockDisplay(Subscriber):
    def __init__(self, name):
        self.name = name

    def update(self, price):
        print(f"{self.name} shows price at ${price}")

class StockAlert(Subscriber):
    def __init__(self, name, threshold):
        self.name = name
        self.threshold = threshold

    def update(self, price):
        if price > self.threshold:
            print(f"{self.name}: Alert! Price ${price} exceeds ${self.threshold}")

if __name__ == "__main__":
    monitor = StockMonitor()
    display = StockDisplay("Terminal")
    alert = StockAlert("Broker", 100)
    monitor.follow(display)
    monitor.follow(alert)
    for p in [50, 90, 99, 100, 101, 99]:
        monitor.price = p
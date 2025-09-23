import weakref
import threading

class Trader:
    def __init__(self, name, priority=0):
        self.name = name
        self.priority = priority

    def receive_update(self, symbol, price):
        print(f"{self.name} received update for {symbol}: ${price}")

class StockMarket:
    def __init__(self):
        self._prices = {}
        self._subscribers = []
        self._lock = threading.Lock()

    def attach_subscriber(self, subscriber, priority=0):
        with self._lock:
            for p, ref in self._subscribers:
                if ref() is subscriber:
                    return
            ref = weakref.ref(subscriber)
            self._subscribers.append((priority, ref))

    def detach_subscriber(self, subscriber):
        with self._lock:
            self._subscribers = [
                (p, ref) for p, ref in self._subscribers
                if ref() is not subscriber
            ]

    def set_price(self, symbol, price):
        with self._lock:
            old_price = self._prices.get(symbol)
            self._prices[symbol] = price
            if old_price != price:
                self._notify(symbol, price)

    def _notify(self, symbol, price):
        with self._lock:
            alive = [
                (p, ref()) for p, ref in self._subscribers
                if ref() is not None
            ]
            alive.sort(key=lambda x: x[0], reverse=True)
        for _, sub in alive:
            try:
                sub.receive_update(symbol, price)
            except Exception:
                pass

if __name__ == "__main__":
    market = StockMarket()
    alice = Trader("Alice", 10)
    charlie = Trader("Charlie", 10)
    bob = Trader("Bob", 5)
    dave = Trader("Dave", 0)

    market.attach_subscriber(alice, alice.priority)
    market.attach_subscriber(charlie, charlie.priority)
    market.attach_subscriber(bob, bob.priority)
    market.attach_subscriber(dave, dave.priority)

    print("Initial update:")
    market.set_price("AAPL", 150)

    print("\nAfter detach Bob:")
    market.detach_subscriber(bob)
    market.set_price("AAPL", 155)

    print("\nAfter del Dave:")
    del dave
    market.set_price("AAPL", 160)
import random

class StockPrice:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self._price = price
        self._watchers = []
    
    def add_watcher(self, watcher):
        if watcher not in self._watchers:
            self._watchers.append(watcher)
    
    def remove_watcher(self, watcher):
        if watcher in self._watchers:
            self._watchers.remove(watcher)
    
    def update_price(self, new_price):
        self._price = new_price
        self._notify_all()
    
    def _notify_all(self):
        for watcher in self._watchers:
            watcher.alert(self)
    
    @property
    def price(self):
        return self._price


class Investor:
    def __init__(self, name, alert_threshold):
        self.name = name
        self.alert_threshold = alert_threshold
    
    def alert(self, stock):
        if stock.price >= self.alert_threshold:
            print(f"{self.name} notified: {stock.symbol} hits {stock.price}")


if __name__ == "__main__":
    stock = StockPrice("TECH", 100)
    alice = Investor("Alice", 105)
    bob = Investor("Bob", 110)
    
    stock.add_watcher(alice)
    stock.add_watcher(bob)
    
    for _ in range(3):
        stock.update_price(random.randint(100, 115))
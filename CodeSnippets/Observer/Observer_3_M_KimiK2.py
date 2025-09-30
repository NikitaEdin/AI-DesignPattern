class StockPrice:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self._price = price
        self._watchers = []

    def add_watcher(self, watcher):
        self._watchers.append(watcher)

    def remove_watcher(self, watcher):
        self._watchers.remove(watcher)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        self._notify_all()

    def _notify_all(self):
        for watcher in self._watchers:
            watcher.update(self)


class PriceDisplay:
    def __init__(self, name):
        self.name = name

    def update(self, stock):
        print(f"{self.name} notified: {stock.symbol} is now ${stock.price}")


class PriceLogger:
    def __init__(self):
        self.history = []

    def update(self, stock):
        self.history.append((stock.symbol, stock.price))


if __name__ == "__main__":
    stock = StockPrice("AAPL", 150)
    display = PriceDisplay("Screen")
    logger = PriceLogger()

    stock.add_watcher(display)
    stock.add_watcher(logger)

    stock.price = 155
    stock.price = 160
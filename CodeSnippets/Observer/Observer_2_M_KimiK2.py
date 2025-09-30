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


class StockDisplay:
    def __init__(self, name):
        self.name = name

    def update(self, stock):
        print(f"{self.name} received update: {stock.symbol} is now ${stock.price}")


if __name__ == "__main__":
    stock = StockPrice("AAPL", 150.00)
    phone = StockDisplay("Phone")
    laptop = StockDisplay("Laptop")
    stock.add_watcher(phone)
    stock.add_watcher(laptop)
    stock.price = 152.50
    stock.price = 148.75
class StockMarket:
    def __init__(self, symbol, price):
        self._symbol = symbol
        self._price = price
        self._investors = []

    def attach(self, investor):
        if investor not in self._investors:
            self._investors.append(investor)
        else:
            raise ValueError("Investor already attached")

    def detach(self, investor):
        if investor in self._investors:
            self._investors.remove(investor)
        else:
            raise ValueError("Investor not found")

    def set_price(self, price):
        self._price = price
        self._notify()

    def _notify(self):
        for investor in self._investors:
            investor.update(self._symbol, self._price)

    def get_price(self):
        return self._price


class Investor:
    def __init__(self, name):
        self._name = name

    def update(self, symbol, price):
        print(f"{self._name} notified: {symbol} price changed to {price}")


if __name__ == "__main__":
    market = StockMarket("AAPL", 150.0)
    investor1 = Investor("Alice")
    investor2 = Investor("Bob")

    market.attach(investor1)
    market.attach(investor2)

    print(f"Initial price for AAPL: {market.get_price()}")
    market.set_price(155.0)
    market.detach(investor2)
    market.set_price(160.0)
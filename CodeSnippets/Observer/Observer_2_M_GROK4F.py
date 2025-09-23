class StockPriceManager:
    def __init__(self, symbol, initial_price):
        self.symbol = symbol
        self.price = initial_price
        self.subscribers = []

    def attach_subscriber(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
        else:
            raise ValueError("Subscriber already attached")

    def detach_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
        else:
            raise ValueError("Subscriber not found")

    def update_price(self, new_price):
        self.price = new_price
        self.notify_subscribers()

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.receive_update(self.symbol, self.price)

class PortfolioTracker:
    def __init__(self, owner):
        self.owner = owner

    def receive_update(self, symbol, price):
        print(f"{self.owner}'s portfolio: {symbol} now at ${price}")

class PriceAlert:
    def __init__(self, threshold):
        self.threshold = threshold

    def receive_update(self, symbol, price):
        if price >= self.threshold:
            print(f"Alert: {symbol} reached ${price} (threshold: ${self.threshold})")

if __name__ == "__main__":
    manager = StockPriceManager("AAPL", 150.0)
    tracker = PortfolioTracker("Alice")
    alert = PriceAlert(160.0)

    manager.attach_subscriber(tracker)
    manager.attach_subscriber(alert)

    manager.update_price(155.0)
    manager.update_price(162.0)

    manager.detach_subscriber(tracker)
    manager.update_price(170.0)
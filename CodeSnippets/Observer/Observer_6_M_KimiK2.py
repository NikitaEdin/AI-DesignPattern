class PriceTracker:
    def __init__(self):
        self._subscribers = []
        self._price = 0

    def attach(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def detach(self, subscriber):
        try:
            self._subscribers.remove(subscriber)
        except ValueError:
            pass

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._price)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value != self._price:
            self._price = value
            self.notify()


class EmailAlert:
    def __init__(self, email):
        self.email = email

    def update(self, price):
        print(f"Email to {self.email}: Price changed to ${price}")


class SMSAlert:
    def __init__(self, phone):
        self.phone = phone

    def update(self, price):
        print(f"SMS to {self.phone}: Price changed to ${price}")


if __name__ == "__main__":
    tracker = PriceTracker()
    tracker.attach(EmailAlert("user@example.com"))
    tracker.attach(SMSAlert("+1234567890"))
    tracker.price = 99
    tracker.price = 149
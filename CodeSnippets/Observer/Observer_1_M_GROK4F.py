class NewsPublisher:
    def __init__(self):
        self._subscribers = []
        self._latest_news = None

    def attach(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def detach(self, subscriber):
        try:
            self._subscribers.remove(subscriber)
        except ValueError:
            pass

    def set_news(self, news):
        self._latest_news = news
        self.notify()

    def notify(self):
        for subscriber in self._subscribers[:]:
            try:
                subscriber.update(self._latest_news)
            except Exception:
                pass

class NewsSubscriber:
    def __init__(self, name):
        self.name = name

    def update(self, news):
        print(f"{self.name} received: {news}")

if __name__ == "__main__":
    publisher = NewsPublisher()
    sub1 = NewsSubscriber("Alice")
    sub2 = NewsSubscriber("Bob")
    publisher.attach(sub1)
    publisher.attach(sub2)
    publisher.set_news("Breaking news!")
    publisher.detach(sub1)
    publisher.set_news("Another update")
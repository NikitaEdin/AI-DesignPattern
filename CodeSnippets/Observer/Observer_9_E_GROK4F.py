class NewsAgency:
    def __init__(self):
        self.headline = None
        self.subscribers = []

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def set_headline(self, headline):
        self.headline = headline
        self.notify_subscribers()

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.receive_news(self.headline)

class NewsChannel:
    def receive_news(self, headline):
        print(f"Channel received: {headline}")

if __name__ == "__main__":
    agency = NewsAgency()
    channel1 = NewsChannel()
    channel2 = NewsChannel()
    agency.add_subscriber(channel1)
    agency.add_subscriber(channel2)
    agency.set_headline("Breaking News!")
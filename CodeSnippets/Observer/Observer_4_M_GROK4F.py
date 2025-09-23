class NewsPublisher:
    def __init__(self):
        self.subscribers = []
        self.current_news = ""

    def add_subscriber(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
        else:
            raise ValueError("Subscriber not found")

    def notify_all(self):
        for subscriber in self.subscribers:
            try:
                subscriber.receive_update(self.current_news)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")

    def publish_news(self, news):
        self.current_news = news
        self.notify_all()

class NewsSubscriber:
    def __init__(self, name):
        self.name = name

    def receive_update(self, news):
        print(f"{self.name} received news: {news}")

class TVChannel(NewsSubscriber):
    def receive_update(self, news):
        super().receive_update(news)
        if "breaking" in news.lower():
            print(f"{self.name} - Alerting viewers!")

if __name__ == "__main__":
    agency = NewsPublisher()
    cnn = TVChannel("CNN")
    bbc = NewsSubscriber("BBC")
    agency.add_subscriber(cnn)
    agency.add_subscriber(bbc)
    agency.publish_news("Breaking: Major event!")
    agency.remove_subscriber(bbc)
    agency.publish_news("Regular update")
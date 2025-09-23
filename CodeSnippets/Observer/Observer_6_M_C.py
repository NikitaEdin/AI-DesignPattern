class NewsChannel:
    def __init__(self, name):
        self.name = name
        self._subscribers = []
        self._latest_news = ""
    
    def add_subscriber(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
    
    def remove_subscriber(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
    
    def notify_all(self):
        for subscriber in self._subscribers:
            try:
                subscriber.receive_update(self)
            except Exception as e:
                print(f"Failed to notify {subscriber.name}: {e}")
    
    def publish_news(self, news):
        self._latest_news = news
        self.notify_all()
    
    def get_latest_news(self):
        return self._latest_news

class Subscriber:
    def __init__(self, name):
        self.name = name
        self.received_news = []
    
    def receive_update(self, channel):
        news = channel.get_latest_news()
        self.received_news.append(f"From {channel.name}: {news}")
        print(f"{self.name} received: {news}")

if __name__ == "__main__":
    news_channel = NewsChannel("Tech Daily")
    
    alice = Subscriber("Alice")
    bob = Subscriber("Bob")
    charlie = Subscriber("Charlie")
    
    news_channel.add_subscriber(alice)
    news_channel.add_subscriber(bob)
    news_channel.add_subscriber(charlie)
    
    news_channel.publish_news("Python 3.12 released!")
    
    news_channel.remove_subscriber(bob)
    
    news_channel.publish_news("AI breakthrough announced!")
    
    print(f"\nAlice's news history: {alice.received_news}")
class NewsAgency:
    def __init__(self):
        self._subscribers = []
        self._latest_news = ""
    
    def subscribe(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
    
    def notify_all(self):
        for subscriber in self._subscribers:
            try:
                subscriber.update(self._latest_news)
            except Exception as e:
                print(f"Failed to notify subscriber: {e}")
    
    def publish_news(self, news):
        self._latest_news = news
        self.notify_all()

class NewsChannel:
    def __init__(self, name):
        self.name = name
    
    def update(self, news):
        print(f"{self.name} received breaking news: {news}")

class Newspaper:
    def __init__(self, name):
        self.name = name
    
    def update(self, news):
        print(f"{self.name} will print: {news}")

if __name__ == "__main__":
    agency = NewsAgency()
    
    cnn = NewsChannel("CNN")
    bbc = NewsChannel("BBC")
    times = Newspaper("The Times")
    
    agency.subscribe(cnn)
    agency.subscribe(bbc)
    agency.subscribe(times)
    
    agency.publish_news("Major earthquake hits Japan")
    
    agency.unsubscribe(bbc)
    
    agency.publish_news("New technology breakthrough announced")
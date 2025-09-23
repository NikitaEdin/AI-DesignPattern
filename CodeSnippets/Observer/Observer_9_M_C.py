class NewsAgency:
    def __init__(self):
        self._subscribers = []
        self._news = ""
    
    def subscribe(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
    
    def notify_all(self):
        for subscriber in self._subscribers:
            try:
                subscriber.update(self._news)
            except Exception:
                pass
    
    def set_news(self, news):
        self._news = news
        self.notify_all()

class Channel:
    def __init__(self, name):
        self.name = name
        self.latest_news = ""
    
    def update(self, news):
        self.latest_news = news
        print(f"{self.name} received: {news}")

class MobileApp:
    def __init__(self, app_name):
        self.app_name = app_name
        self.notifications = []
    
    def update(self, news):
        self.notifications.append(news)
        print(f"{self.app_name} notification: {news}")

if __name__ == "__main__":
    agency = NewsAgency()
    
    tv_channel = Channel("TV News")
    radio_channel = Channel("Radio News")
    mobile_app = MobileApp("NewsApp")
    
    agency.subscribe(tv_channel)
    agency.subscribe(radio_channel)
    agency.subscribe(mobile_app)
    
    agency.set_news("Breaking: New technology breakthrough!")
    
    agency.unsubscribe(radio_channel)
    
    agency.set_news("Weather alert: Storm approaching!")
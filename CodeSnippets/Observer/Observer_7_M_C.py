class NewsPublisher:
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
                print(f"Error notifying subscriber: {e}")
    
    def publish_news(self, news):
        self._latest_news = news
        self.notify_all()

class EmailSubscriber:
    def __init__(self, email):
        self.email = email
    
    def update(self, news):
        print(f"Email to {self.email}: Breaking News - {news}")

class SMSSubscriber:
    def __init__(self, phone):
        self.phone = phone
    
    def update(self, news):
        print(f"SMS to {self.phone}: {news[:50]}...")

class WebSubscriber:
    def __init__(self, website):
        self.website = website
    
    def update(self, news):
        print(f"Website {self.website} updated: {news}")

if __name__ == "__main__":
    publisher = NewsPublisher()
    
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("+1234567890")
    web_sub = WebSubscriber("news.com")
    
    publisher.subscribe(email_sub)
    publisher.subscribe(sms_sub)
    publisher.subscribe(web_sub)
    
    publisher.publish_news("Major earthquake hits downtown area")
    
    publisher.unsubscribe(sms_sub)
    publisher.publish_news("Weather alert: Heavy rain expected")
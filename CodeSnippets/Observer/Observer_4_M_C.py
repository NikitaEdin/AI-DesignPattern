class NewsPublisher:
    def __init__(self):
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
                subscriber.update(self._latest_news)
            except AttributeError:
                self.remove_subscriber(subscriber)
    
    def publish_news(self, news):
        self._latest_news = news
        self.notify_all()

class EmailSubscriber:
    def __init__(self, email):
        self.email = email
    
    def update(self, news):
        print(f"Email sent to {self.email}: {news}")

class SMSSubscriber:
    def __init__(self, phone):
        self.phone = phone
    
    def update(self, news):
        print(f"SMS sent to {self.phone}: {news}")

class WebAppSubscriber:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def update(self, news):
        print(f"Web notification for user {self.user_id}: {news}")

if __name__ == "__main__":
    publisher = NewsPublisher()
    
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("123-456-7890")
    web_sub = WebAppSubscriber("user123")
    
    publisher.add_subscriber(email_sub)
    publisher.add_subscriber(sms_sub)
    publisher.add_subscriber(web_sub)
    
    publisher.publish_news("Breaking: New technology announced!")
    
    publisher.remove_subscriber(sms_sub)
    publisher.publish_news("Update: Technology release delayed")
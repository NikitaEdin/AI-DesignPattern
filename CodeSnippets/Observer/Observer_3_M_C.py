class Publisher:
    def __init__(self):
        self._subscribers = []
        self._state = None
    
    def subscribe(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        try:
            self._subscribers.remove(subscriber)
        except ValueError:
            pass
    
    def notify(self):
        for subscriber in self._subscribers:
            try:
                subscriber.update(self._state)
            except Exception:
                pass
    
    def set_state(self, state):
        self._state = state
        self.notify()

class EmailSubscriber:
    def __init__(self, email):
        self.email = email
    
    def update(self, data):
        print(f"Email sent to {self.email}: {data}")

class SMSSubscriber:
    def __init__(self, phone):
        self.phone = phone
    
    def update(self, data):
        print(f"SMS sent to {self.phone}: {data}")

class WebhookSubscriber:
    def __init__(self, url):
        self.url = url
    
    def update(self, data):
        print(f"Webhook called at {self.url}: {data}")

if __name__ == "__main__":
    news_service = Publisher()
    
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("+1234567890")
    webhook_sub = WebhookSubscriber("https://api.example.com/webhook")
    
    news_service.subscribe(email_sub)
    news_service.subscribe(sms_sub)
    news_service.subscribe(webhook_sub)
    
    news_service.set_state("Breaking: New product launch!")
    
    news_service.unsubscribe(sms_sub)
    news_service.set_state("Update: Product details revealed!")
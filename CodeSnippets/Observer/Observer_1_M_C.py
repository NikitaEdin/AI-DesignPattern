class Publisher:
    def __init__(self):
        self._subscribers = []
        self._state = None

    def subscribe(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify(self, event_data):
        for subscriber in self._subscribers:
            try:
                subscriber.update(self, event_data)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")

    def set_state(self, new_state):
        self._state = new_state
        self.notify(new_state)

    def get_state(self):
        return self._state

class NewsSubscriber:
    def __init__(self, name):
        self.name = name

    def update(self, publisher, data):
        print(f"{self.name} received news update: {data}")

class EmailSubscriber:
    def __init__(self, email):
        self.email = email

    def update(self, publisher, data):
        print(f"Sending email to {self.email}: Breaking News - {data}")

if __name__ == "__main__":
    news_agency = Publisher()
    
    reader1 = NewsSubscriber("John")
    reader2 = NewsSubscriber("Alice")
    email_service = EmailSubscriber("admin@news.com")
    
    news_agency.subscribe(reader1)
    news_agency.subscribe(reader2)
    news_agency.subscribe(email_service)
    
    news_agency.set_state("Market reaches all-time high")
    news_agency.set_state("New technology breakthrough announced")
    
    news_agency.unsubscribe(reader1)
    news_agency.set_state("Weather alert issued")
class Newsletter:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        self._latest_article = None
    
    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            return True
        return False
    
    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            return True
        return False
    
    def notify_all(self):
        for subscriber in self.subscribers[:]:
            try:
                subscriber.update(self, self._latest_article)
            except Exception:
                self.subscribers.remove(subscriber)
    
    def publish_article(self, article):
        self._latest_article = article
        self.notify_all()

class Reader:
    def __init__(self, name):
        self.name = name
        self.received_articles = []
    
    def update(self, newsletter, article):
        self.received_articles.append(f"{newsletter.name}: {article}")
        print(f"{self.name} received article '{article}' from {newsletter.name}")

class EmailReader(Reader):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email
    
    def update(self, newsletter, article):
        super().update(newsletter, article)
        print(f"Email sent to {self.email}")

if __name__ == "__main__":
    tech_news = Newsletter("TechDaily")
    
    alice = Reader("Alice")
    bob = EmailReader("Bob", "bob@email.com")
    charlie = Reader("Charlie")
    
    tech_news.subscribe(alice)
    tech_news.subscribe(bob)
    tech_news.subscribe(charlie)
    
    tech_news.publish_article("Python 3.12 Released")
    
    tech_news.unsubscribe(charlie)
    tech_news.publish_article("AI Breakthrough in 2024")
class NewsAgency:
    def __init__(self):
        self.subscribers = []
        self.news = ""

    def attach(self, subscriber):
        self.subscribers.append(subscriber)

    def detach(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.news)

    def set_news(self, news):
        self.news = news
        self.notify()

class NewsSubscriber:
    def __init__(self, name):
        self.name = name

    def update(self, news):
        print(f"{self.name} received: {news}")

if __name__ == "__main__":
    agency = NewsAgency()
    sub1 = NewsSubscriber("Subscriber1")
    sub2 = NewsSubscriber("Subscriber2")
    agency.attach(sub1)
    agency.attach(sub2)
    agency.set_news("Breaking news!")
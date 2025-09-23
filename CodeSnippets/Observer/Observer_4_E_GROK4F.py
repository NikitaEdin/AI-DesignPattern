class NewsAgency:
    def __init__(self):
        self.subscribers = []
        self.headline = ""

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.receive_news(self.headline)

class Subscriber:
    def __init__(self, name):
        self.name = name

    def receive_news(self, headline):
        print(f"{self.name} received: {headline}")

if __name__ == "__main__":
    agency = NewsAgency()
    sub1 = Subscriber("Alice")
    sub2 = Subscriber("Bob")
    agency.add_subscriber(sub1)
    agency.add_subscriber(sub2)
    agency.headline = "Breaking News!"
    agency.notify_subscribers()
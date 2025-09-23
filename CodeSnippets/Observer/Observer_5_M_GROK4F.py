class NewsFeed:
    def __init__(self):
        self._subscribers = []

    def register(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unregister(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def publish(self, news):
        for subscriber in self._subscribers[:]:
            try:
                subscriber.notify(news)
            except Exception:
                pass

class PrintOutlet:
    def notify(self, news):
        print(f"Printed news: {news}")

class EmailOutlet:
    def notify(self, news):
        print(f"Email sent with news: {news}")

if __name__ == "__main__":
    feed = NewsFeed()
    print_outlet = PrintOutlet()
    email_outlet = EmailOutlet()

    feed.register(print_outlet)
    feed.register(email_outlet)

    feed.publish("Breaking news: Event occurred!")

    feed.unregister(email_outlet)

    feed.publish("Update: New developments.")
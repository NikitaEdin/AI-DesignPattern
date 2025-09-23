class NewsPublisher:
    def __init__(self):
        self._subscribers = []
        self._latest_news = ""

    def attach(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
        else:
            raise ValueError("Subscriber already attached.")

    def detach(self, subscriber):
        try:
            self._subscribers.remove(subscriber)
        except ValueError:
            pass  # Ignore if not found

    def set_news(self, news):
        self._latest_news = news
        self._notify()

    def _notify(self):
        for subscriber in self._subscribers[:]:  # Copy to avoid modification issues
            subscriber.receive_update(self._latest_news)

class TVChannel:
    def __init__(self, name):
        self.name = name

    def receive_update(self, news):
        print(f"{self.name} broadcasting: {news}")

class PrintMedia:
    def __init__(self, name):
        self.name = name

    def receive_update(self, news):
        print(f"{self.name} printing: {news}")

if __name__ == "__main__":
    publisher = NewsPublisher()
    channel1 = TVChannel("CNN")
    channel2 = TVChannel("BBC")
    media = PrintMedia("NY Times")

    publisher.attach(channel1)
    publisher.attach(channel2)
    publisher.attach(media)

    publisher.set_news("Breaking: Major event occurred!")

    publisher.detach(channel2)
    publisher.set_news("Update: Event details revealed.")
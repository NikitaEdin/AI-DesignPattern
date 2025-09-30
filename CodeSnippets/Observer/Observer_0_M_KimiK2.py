class NewsPublisher:
    def __init__(self):
        self._readers = []

    def subscribe(self, reader):
        if reader not in self._readers:
            self._readers.append(reader)

    def unsubscribe(self, reader):
        try:
            self._readers.remove(reader)
        except ValueError:
            pass

    def notify(self, news):
        for reader in self._readers:
            reader.update(news)


class BaseReader:
    def update(self, news):
        pass


class EmailReader(BaseReader):
    def __init__(self, address):
        self.address = address
        self.articles = []

    def update(self, news):
        self.articles.append(news)
        self.send_email(news)

    def send_email(self, news):
        pass


class SMSTicker(BaseReader):
    def __init__(self, phone):
        self.phone = phone
        self.last = None

    def update(self, news):
        self.last = news


if __name__ == "__main__":
    pub = NewsPublisher()
    alice = EmailReader("alice@mail.com")
    bob = SMSTicker("555-1234")

    pub.subscribe(alice)
    pub.subscribe(bob)

    pub.notify("Breaking: Python 4 is out")
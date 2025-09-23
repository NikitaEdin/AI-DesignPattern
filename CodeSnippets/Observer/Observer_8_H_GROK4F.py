import weakref
from weakref import WeakSet, WeakKeyDictionary

class Broadcaster:
    def __init__(self):
        self._listeners = WeakSet()
        self._priorities = WeakKeyDictionary()

    def add_listener(self, listener, priority=0):
        self._listeners.add(listener)
        self._priorities[listener] = priority

    def remove_listener(self, listener):
        self._listeners.discard(listener)
        self._priorities.pop(listener, None)

    def broadcast(self, message):
        active_listeners = [(lst, self._priorities.get(lst, 0)) for lst in list(self._listeners)]
        active_listeners.sort(key=lambda x: x[1], reverse=True)
        for lst, _ in active_listeners:
            try:
                lst.receive(self, message)
            except Exception:
                pass

class NewsBroadcaster(Broadcaster):
    def __init__(self):
        super().__init__()
        self._latest_news = None

    def update_news(self, news):
        self._latest_news = news
        self.broadcast(news)

class NewsReceiver:
    def __init__(self, name):
        self.name = name

    def receive(self, source, news):
        print(f"{self.name} got news: {news}")

if __name__ == "__main__":
    bc = NewsBroadcaster()
    r1 = NewsReceiver("CNN")
    r2 = NewsReceiver("BBC")
    bc.add_listener(r1, priority=1)
    bc.add_listener(r2, priority=2)
    bc.update_news("Election results are in!")
    bc.remove_listener(r1)
    bc.update_news("Second update: Markets crashing!")
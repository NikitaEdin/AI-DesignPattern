class Publisher:
    def __init__(self):
        self._watchers = []
    def add(self, watcher):
        self._watchers.append(watcher)
    def notify(self, msg):
        for w in self._watchers:
            w.update(msg)

class Subscriber:
    def update(self, msg):
        print("Received:", msg)

if __name__ == "__main__":
    pub = Publisher()
    sub = Subscriber()
    pub.add(sub)
    pub.notify("Hello")
    pub.notify("Goodbye")
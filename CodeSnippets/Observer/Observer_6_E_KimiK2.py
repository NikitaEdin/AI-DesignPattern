class Publisher:
    def __init__(self):
        self._watchers = []
    def attach(self, watcher):
        self._watchers.append(watcher)
    def detach(self, watcher):
        self._watchers.remove(watcher)
    def alert(self, info):
        for w in self._watchers:
            w.update(info)

class Watcher:
    def update(self, info):
        print(f"Got: {info}")

if __name__ == "__main__":
    p = Publisher()
    w1 = Watcher()
    w2 = Watcher()
    p.attach(w1)
    p.attach(w2)
    p.alert("Hello")
class Publisher:
    def __init__(self):
        self._watchers = []

    def add(self, watcher):
        self._watchers.append(watcher)
    
    def remove(self, watcher):
        self._watchers.remove(watcher)
    
    def alert(self, data):
        for w in self._watchers:
            w.update(data)


class Watcher:
    def __init__(self, name):
        self.name = name
    
    def update(self, data):
        print(f"{self.name} received: {data}")


if __name__ == "__main__":
    p = Publisher()
    a = Watcher("A")
    b = Watcher("B")
    p.add(a)
    p.add(b)
    p.alert("hello")
class Subject:
    def __init__(self):
        self.watchers = []
    
    def attach(self, watcher):
        self.watchers.append(watcher)
    
    def notify(self):
        for watcher in self.watchers:
            watcher.update()

class Watcher:
    def __init__(self, name):
        self.name = name
    
    def update(self):
        print(f"{self.name} received notification")

class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self.news = ""
    
    def set_news(self, news):
        self.news = news
        self.notify()

if __name__ == "__main__":
    agency = NewsAgency()
    watcher1 = Watcher("TV Channel")
    watcher2 = Watcher("Radio Station")
    
    agency.attach(watcher1)
    agency.attach(watcher2)
    
    agency.set_news("Breaking News!")
class Subject:
    def __init__(self):
        self._listeners = []
    
    def attach(self, listener):
        self._listeners.append(listener)
    
    def notify(self, data):
        for listener in self._listeners:
            listener.update(data)

class Display:
    def __init__(self, name):
        self.name = name
    
    def update(self, data):
        print(f"{self.name}: {data}")

class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self._news = ""
    
    def set_news(self, news):
        self._news = news
        self.notify(news)

if __name__ == "__main__":
    agency = NewsAgency()
    tv = Display("TV Channel")
    radio = Display("Radio Station")
    
    agency.attach(tv)
    agency.attach(radio)
    
    agency.set_news("Breaking: New discovery announced!")
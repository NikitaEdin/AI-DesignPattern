class Publisher:
    def __init__(self):
        self._subscribers = []
    
    def attach(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
    
    def detach(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
    
    def notify(self, data):
        for subscriber in self._subscribers:
            try:
                subscriber.update(data)
            except Exception as e:
                print(f"Error updating subscriber: {e}")

class Subscriber:
    def update(self, data):
        raise NotImplementedError

class NewsAgency(Publisher):
    def __init__(self, name):
        super().__init__()
        self._name = name
    
    def publish_story(self, story):
        self.notify(story)

class NewsChannel(Subscriber):
    def __init__(self, name):
        self._name = name
    
    def update(self, story):
        print(f"{self._name} broadcasting: {story}")

class WeatherService(Subscriber):
    def __init__(self, name):
        self._name = name
    
    def update(self, data):
        print(f"{self._name} weather update: {data}")

if __name__ == "__main__":
    agency = NewsAgency("Daily News")
    channel1 = NewsChannel("TV News")
    channel2 = NewsChannel("Radio News")
    weather = WeatherService("Weather Central")
    
    agency.attach(channel1)
    agency.attach(channel2)
    agency.attach(weather)
    
    agency.publish_story("Breaking: Local hero saves cat from tree")
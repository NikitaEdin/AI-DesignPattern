from typing import List, Callable, Any, Dict
from functools import wraps
import weakref

class Subject:
    def __init__(self):
        self._watchers: Dict[str, List[weakref.ref]] = {}
        self._event_filters: Dict[str, List[Callable]] = {}
    
    def attach(self, watcher, event_type: str = "default", filter_func: Callable = None):
        if event_type not in self._watchers:
            self._watchers[event_type] = []
            self._event_filters[event_type] = []
        
        self._watchers[event_type].append(weakref.ref(watcher))
        self._event_filters[event_type].append(filter_func)
    
    def detach(self, watcher, event_type: str = "default"):
        if event_type in self._watchers:
            self._watchers[event_type] = [
                ref for ref in self._watchers[event_type] 
                if ref() is not None and ref() is not watcher
            ]
    
    def notify(self, event_type: str = "default", data: Any = None):
        if event_type not in self._watchers:
            return
        
        active_refs = []
        active_filters = []
        
        for ref, filter_func in zip(self._watchers[event_type], self._event_filters[event_type]):
            watcher = ref()
            if watcher is not None:
                if filter_func is None or filter_func(data):
                    watcher.update(self, event_type, data)
                active_refs.append(ref)
                active_filters.append(filter_func)
        
        self._watchers[event_type] = active_refs
        self._event_filters[event_type] = active_filters

def tracked_property(event_type: str = "property_changed"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            old_value = getattr(self, f"_{func.__name__}", None)
            if old_value != value:
                setattr(self, f"_{func.__name__}", value)
                self.notify(event_type, {"property": func.__name__, "old": old_value, "new": value})
        return property(lambda self: getattr(self, f"_{func.__name__}", None), wrapper)
    return decorator

class NewsPublisher(Subject):
    def __init__(self):
        super().__init__()
        self._breaking_news = ""
        self._weather = ""
    
    @tracked_property("breaking_news")
    def breaking_news(self): pass
    
    @tracked_property("weather_update")
    def weather(self): pass
    
    def publish_article(self, category: str, content: str):
        self.notify("article_published", {"category": category, "content": content})

class NewsSubscriber:
    def __init__(self, name: str):
        self.name = name
        self.received_updates = []
    
    def update(self, subject, event_type: str, data: Any):
        self.received_updates.append(f"{self.name} received {event_type}: {data}")

class PrioritySubscriber:
    def __init__(self, name: str, priority_categories: List[str]):
        self.name = name
        self.priority_categories = priority_categories
        self.received_updates = []
    
    def update(self, subject, event_type: str, data: Any):
        if event_type == "article_published" and data["category"] in self.priority_categories:
            self.received_updates.append(f"PRIORITY - {self.name}: {data}")
        elif event_type != "article_published":
            self.received_updates.append(f"{self.name}: {event_type} - {data}")

if __name__ == "__main__":
    publisher = NewsPublisher()
    
    general_subscriber = NewsSubscriber("John")
    tech_subscriber = PrioritySubscriber("Alice", ["technology", "science"])
    sports_subscriber = NewsSubscriber("Bob")
    
    publisher.attach(general_subscriber)
    publisher.attach(tech_subscriber, "article_published", 
                    lambda data: data["category"] in ["technology", "science"])
    publisher.attach(sports_subscriber, "article_published", 
                    lambda data: data["category"] == "sports")
    publisher.attach(general_subscriber, "breaking_news")
    publisher.attach(tech_subscriber, "weather_update")
    
    publisher.breaking_news = "Major earthquake hits region"
    publisher.weather = "Sunny, 25°C"
    publisher.publish_article("technology", "New AI breakthrough announced")
    publisher.publish_article("sports", "Team wins championship")
    
    for update in general_subscriber.received_updates:
        print(update)
    
    print("\nTech subscriber updates:")
    for update in tech_subscriber.received_updates:
        print(update)
    
    print("\nSports subscriber updates:")
    for update in sports_subscriber.received_updates:
        print(update)
from abc import ABC, abstractmethod
import weakref
from typing import Set, List, Dict, Any
from collections import defaultdict, deque

class Listener(ABC):
    @abstractmethod
    def notify(self, event_type: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self, max_history: int = 100):
        self._listeners: Dict[str, Set[weakref.ref]] = defaultdict(set)
        self._event_history: deque = deque(maxlen=max_history)
    
    def subscribe(self, event_type: str, listener: Listener) -> None:
        weak_ref = weakref.ref(listener)
        self._listeners[event_type].add(weak_ref)
    
    def unsubscribe(self, event_type: str, listener: Listener) -> None:
        to_remove = None
        for weak_ref in self._listeners[event_type]:
            if weak_ref() is listener:
                to_remove = weak_ref
                break
        if to_remove:
            self._listeners[event_type].discard(to_remove)
    
    def publish(self, event_type: str, data: Any) -> None:
        self._event_history.append((event_type, data))
        dead_refs = set()
        
        for weak_ref in self._listeners[event_type].copy():
            listener = weak_ref()
            if listener is None:
                dead_refs.add(weak_ref)
            else:
                try:
                    listener.notify(event_type, data)
                except Exception as e:
                    print(f"Error notifying listener: {e}")
        
        self._listeners[event_type] -= dead_refs

class NewsAgency(Publisher):
    def __init__(self):
        super().__init__()
        self._breaking_news: List[str] = []
    
    def add_news(self, news: str, is_breaking: bool = False) -> None:
        if is_breaking:
            self._breaking_news.append(news)
            self.publish("breaking", news)
        else:
            self.publish("regular", news)

class NewsChannel(Listener):
    def __init__(self, name: str):
        self.name = name
        self.received_news: List[str] = []
    
    def notify(self, event_type: str, data: Any) -> None:
        self.received_news.append(f"[{event_type.upper()}] {data}")
        print(f"{self.name} received: [{event_type.upper()}] {data}")

class PriorityChannel(Listener):
    def __init__(self, name: str):
        self.name = name
        self.priority_news: List[str] = []
    
    def notify(self, event_type: str, data: Any) -> None:
        if event_type == "breaking":
            self.priority_news.append(data)
            print(f"🚨 {self.name} PRIORITY ALERT: {data}")

if __name__ == "__main__":
    agency = NewsAgency()
    
    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")
    priority_channel = PriorityChannel("Emergency Broadcast")
    
    agency.subscribe("regular", channel1)
    agency.subscribe("regular", channel2)
    agency.subscribe("breaking", channel1)
    agency.subscribe("breaking", channel2)
    agency.subscribe("breaking", priority_channel)
    
    agency.add_news("Stock market opens higher today")
    agency.add_news("Major earthquake hits region", is_breaking=True)
    
    agency.unsubscribe("regular", channel1)
    agency.add_news("Weather forecast for tomorrow")
    
    del channel2
    agency.add_news("Breaking: New technology announced", is_breaking=True)
    
    print(f"\nChannel1 received {len(channel1.received_news)} news items")
    print(f"Priority channel has {len(priority_channel.priority_news)} alerts")
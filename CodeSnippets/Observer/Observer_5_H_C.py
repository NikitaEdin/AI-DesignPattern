from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set
import weakref
from functools import wraps

class Subject:
    def __init__(self):
        self._listeners: Dict[str, Set[weakref.ReferenceType]] = {}
        self._paused_events: Set[str] = set()
        self._event_history: List[tuple] = []
        
    def subscribe(self, event_type: str, listener, priority: int = 0):
        if event_type not in self._listeners:
            self._listeners[event_type] = set()
        
        def cleanup(ref):
            if event_type in self._listeners:
                self._listeners[event_type].discard(ref)
        
        listener_ref = weakref.ref(listener, cleanup)
        listener_ref.priority = priority
        listener_ref.listener_id = id(listener)
        self._listeners[event_type].add(listener_ref)
    
    def unsubscribe(self, event_type: str, listener):
        if event_type in self._listeners:
            to_remove = None
            for ref in self._listeners[event_type]:
                if ref.listener_id == id(listener):
                    to_remove = ref
                    break
            if to_remove:
                self._listeners[event_type].discard(to_remove)
    
    def notify(self, event_type: str, data: Any = None):
        if event_type in self._paused_events:
            return
            
        self._event_history.append((event_type, data))
        
        if event_type in self._listeners:
            sorted_listeners = sorted(
                [ref for ref in self._listeners[event_type] if ref() is not None],
                key=lambda x: getattr(x, 'priority', 0),
                reverse=True
            )
            
            for listener_ref in sorted_listeners:
                listener = listener_ref()
                if listener:
                    listener.handle_event(event_type, data, self)
    
    def pause_events(self, *event_types):
        self._paused_events.update(event_types)
    
    def resume_events(self, *event_types):
        self._paused_events.difference_update(event_types)
    
    def get_event_history(self, limit: int = None):
        return self._event_history[-limit:] if limit else self._event_history[:]

class Listener(ABC):
    @abstractmethod
    def handle_event(self, event_type: str, data: Any, source: Subject):
        pass

class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self._breaking_news = []
        self._regular_news = []
    
    def publish_breaking_news(self, headline: str):
        self._breaking_news.append(headline)
        self.notify("breaking_news", headline)
    
    def publish_regular_news(self, article: str):
        self._regular_news.append(article)
        self.notify("regular_news", article)
    
    def retract_news(self, news_id: str):
        self.notify("retraction", news_id)

class EmailSubscriber(Listener):
    def __init__(self, email: str):
        self.email = email
        self.received_notifications = []
    
    def handle_event(self, event_type: str, data: Any, source: Subject):
        message = f"Email to {self.email}: {event_type.upper()} - {data}"
        self.received_notifications.append(message)

class MobileApp(Listener):
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.push_notifications = []
    
    def handle_event(self, event_type: str, data: Any, source: Subject):
        if event_type == "breaking_news":
            notification = f"🚨 BREAKING: {data}"
        else:
            notification = f"📰 {data}"
        self.push_notifications.append(notification)

if __name__ == "__main__":
    agency = NewsAgency()
    
    email_sub = EmailSubscriber("user@example.com")
    mobile_app = MobileApp("user123")
    premium_email = EmailSubscriber("premium@example.com")
    
    agency.subscribe("breaking_news", email_sub, priority=1)
    agency.subscribe("breaking_news", mobile_app, priority=3)
    agency.subscribe("breaking_news", premium_email, priority=5)
    agency.subscribe("regular_news", email_sub)
    agency.subscribe("retraction", premium_email)
    
    agency.publish_breaking_news("Major earthquake hits coastal region")
    agency.publish_regular_news("Local festival scheduled for next weekend")
    
    agency.pause_events("regular_news")
    agency.publish_regular_news("This won't notify anyone")
    
    agency.resume_events("regular_news")
    agency.publish_regular_news("Weather forecast: sunny skies ahead")
    
    agency.retract_news("NEWS_001")
    
    print("Email notifications:", len(email_sub.received_notifications))
    print("Mobile notifications:", len(mobile_app.push_notifications))
    print("Premium notifications:", len(premium_email.received_notifications))
    print("Event history:", len(agency.get_event_history()))
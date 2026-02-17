### OBSERVER PATTERN IMPLEMENTATION ###

from abc import ABC, abstractmethod
from typing import List

# Observer interface
class NewsSubscriber(ABC):
    """
    Abstract base class for all news subscribers.
    Defines the interface for receiving updates.
    """
    @abstractmethod
    def update(self, headline: str) -> None:
        """Receive new headline from publisher"""
        pass

# Subject interface
class NewsPublisher(ABC):
    """
    Abstract base class for news publishers.
    Defines the interface for managing subscribers.
    """
    @abstractmethod
    def attach(self, subscriber: NewsSubscriber) -> None:
        """Attach a subscriber to the publisher"""
        pass
    
    @abstractmethod
    def detach(self, subscriber: NewsSubscriber) -> None:
        """Detach a subscriber from the publisher"""
        pass
    
    @abstractmethod
    def notify(self) -> None:
        """Notify all subscribers about an update"""
        pass


class ConcreteNewsPublisher(NewsPublisher):
    """
    Concrete implementation of NewsPublisher using Observer pattern.
    Manages subscribers and automatically pushes updates to them.
    """
    def __init__(self):
        self._subscribers: List[NewsSubscriber] = []
        self._latest_headline = "No breaking news."
    
    def attach(self, subscriber: NewsSubscriber) -> None:
        """Subscribe a new observer to receive updates"""
        print(f"Publisher: {subscriber.__class__.__name__} subscribed.")
        self._subscribers.append(subscriber)
    
    def detach(self, subscriber: NewsSubscriber) -> None:
        """Unsubscribe an observer from updates"""
        print(f"Publisher: {subscriber.__class__.__name__} unsubscribed.")
        self._subscribers.remove(subscriber)
    
    def notify(self) -> None:
        """Push updates to all subscribed observers"""
        print(f"Publisher: Broadcasting to {len(self._subscribers)} subscriber(s)...")
        for subscriber in self._subscribers:
            subscriber.update(self._latest_headline)
    
    def publish_headline(self, new_headline: str) -> None:
        """
        Update the headline and automatically notify all subscribers.
        This replaces the pull-based approach with push-based updates.
        """
        print(f"\nPUBLISHER: Central headline updated to: '{new_headline}'")
        self._latest_headline = new_headline
        self.notify()


class EmailAlertSubscriber(NewsSubscriber):
    """
    Concrete subscriber that receives email alerts.
    Implements the Observer interface to receive push notifications.
    """
    def __init__(self, name: str = "Email Alert Service"):
        self.name = name
    
    def update(self, headline: str) -> None:
        """Receive and process new headline (automatic push notification)"""
        print(f"[{self.name}] PUSH NOTIFICATION: New headline received: {headline}")


class HomepageWidgetSubscriber(NewsSubscriber):
    """
    Concrete subscriber that updates a homepage widget.
    Implements the Observer interface to receive push notifications.
    """
    def __init__(self, name: str = "Homepage Widget"):
        self.name = name
    
    def update(self, headline: str) -> None:
        """Receive and display new headline (automatic push notification)"""
        print(f"[{self.name}] PUSH NOTIFICATION: Widget updated with: {headline}")


class MobileAppSubscriber(NewsSubscriber):
    """
    Additional subscriber type demonstrating extensibility.
    New subscriber types can be added without modifying the publisher.
    """
    def __init__(self, name: str = "Mobile App"):
        self.name = name
    
    def update(self, headline: str) -> None:
        """Receive and push mobile notification"""
        print(f"[{self.name}] PUSH NOTIFICATION: 📱 Breaking: {headline}")


# --- Demonstration of the Observer Pattern ---

print("--- Observer Pattern Demonstration (Push Method) ---")

# 1. Initialize Publisher
news_publisher = ConcreteNewsPublisher()

# 2. Create Subscribers
email_alert = EmailAlertSubscriber()
homepage_widget = HomepageWidgetSubscriber()
mobile_app = MobileAppSubscriber()

# 3. Subscribe observers to the publisher
news_publisher.attach(email_alert)
news_publisher.attach(homepage_widget)
news_publisher.attach(mobile_app)

# 4. Publishing automatically notifies all subscribers
print("\n1. Publishing first story:")
news_publisher.publish_headline("Local Cat Rescued from Tree!")

print("\n2. Publishing second story:")
news_publisher.publish_headline("Major City Council Decision Today.")

# 5. Demonstrate dynamic subscription management
print("\n3. Unsubscribing mobile app:")
news_publisher.detach(mobile_app)

print("\n4. Publishing third story (mobile app won't receive it):")
news_publisher.publish_headline("Weather Alert: Storm Approaching!")

# 6. Demonstrate that subscribers no longer need to poll
print("\n--- Comparison with old Singleton approach ---")
print("OLD WAY: Subscribers had to manually check for updates")
print("NEW WAY: Updates are automatically pushed to subscribers")

# Simulate what would happen with the old approach
print("\nSimulating old pull-based behavior:")
print("Subscriber checking for news (old way)...")
# This would have been: subscriber.check_for_news()
print("With Observer pattern, subscribers don't need to check - they receive updates automatically!")
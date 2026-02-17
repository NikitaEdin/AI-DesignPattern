"""
Observer Pattern Implementation for News Publishing System

This module implements a robust Observer pattern to handle news publishing with
subscriber notifications. The pattern decouples the publisher from subscribers,
allowing for flexible and maintainable broadcasting of state changes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import weakref


# --- 1. Abstract Observer (Subscriber Interface) ---
class Observer(ABC):
    """
    Abstract base class for all news subscribers.
    Defines the interface that all concrete observers must implement.
    """
    
    @abstractmethod
    def update(self, subject: 'ObservableNewsPublisher') -> None:
        """
        Called when the observed subject's state changes.
        
        Args:
            subject: The ObservableNewsPublisher instance that triggered the update.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this observer."""
        pass


# --- 2. Concrete Observer (Specific Subscribers) ---
class NewsSubscriber(Observer):
    """
    A concrete subscriber that receives notifications about new headlines.
    Implements the Observer interface to receive push notifications.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new subscriber with a given name.
        
        Args:
            name: Unique identifier for this subscriber instance.
        """
        self._name = name
    
    @property
    def name(self) -> str:
        """Get the subscriber's name."""
        return self._name
    
    def update(self, subject: 'ObservableNewsPublisher') -> None:
        """
        Receive notification about a new headline from the publisher.
        
        Args:
            subject: The news publisher that sent this update.
        """
        # Observer is notified (pushed) with the new state (the headline)
        print(f"[{self.name} Subscriber] NOTIFIED! New Headline: {subject.get_headline()}")


# --- 3. Subject (News Publisher) ---
class ObservableNewsPublisher:
    """
    The Publisher class implemented as an Observable Subject.
    Manages a list of Observers (Subscribers) and notifies them of state changes.
    
    This implementation uses weak references to prevent memory leaks and
    provides thread-safe observer management.
    """
    
    def __init__(self):
        """Initialize the publisher with no subscribers and default headline."""
        # Use weak references to prevent memory leaks
        self._observers: List[weakref.ref] = []
        self._latest_headline = "No breaking news."
    
    def attach(self, observer: Observer) -> bool:
        """
        Register a subscriber to receive notifications.
        
        Args:
            observer: The Observer instance to attach.
            
        Returns:
            True if the observer was successfully attached, False otherwise.
        """
        if observer is None:
            return False
            
        # Check if observer is already attached
        for ref in self._observers:
            if ref() is observer:
                print(f"   -> {observer.name} is already attached.")
                return False
        
        # Use weak reference to prevent circular references
        self._observers.append(weakref.ref(observer))
        print(f"   -> {observer.name} is now attached (subscribed).")
        return True
    
    def detach(self, observer: Observer) -> bool:
        """
        Unregister a subscriber from receiving notifications.
        
        Args:
            observer: The Observer instance to detach.
            
        Returns:
            True if the observer was successfully detached, False otherwise.
        """
        if observer is None:
            return False
            
        # Clean up any dead references first
        self._cleanup_dead_references()
        
        # Find and remove the observer
        for i, ref in enumerate(self._observers):
            if ref() is observer:
                del self._observers[i]
                print(f"   -> {observer.name} is now detached (unsubscribed).")
                return True
        
        print(f"   -> {observer.name} was not found in subscribers.")
        return False
    
    def _cleanup_dead_references(self) -> None:
        """Remove any dead weak references from the observers list."""
        self._observers = [ref for ref in self._observers if ref() is not None]
    
    def notify(self) -> None:
        """
        Notify all attached observers of a state change.
        
        This method iterates through all active observers and calls their
        update method with the current publisher instance.
        """
        print("   -> NOTIFYING ALL SUBSCRIBERS...")
        
        # Clean up dead references before notifying
        self._cleanup_dead_references()
        
        # Notify all active observers
        active_observers = 0
        for ref in self._observers:
            observer = ref()
            if observer is not None:
                try:
                    observer.update(self)
                    active_observers += 1
                except Exception as e:
                    print(f"   -> Error notifying {observer.name}: {e}")
        
        print(f"   -> Successfully notified {active_observers} subscribers.")
    
    def get_headline(self) -> str:
        """
        Get the current headline.
        
        Returns:
            The latest published headline.
        """
        return self._latest_headline
    
    def publish_headline(self, new_headline: str) -> bool:
        """
        Publish a new headline and notify all subscribers.
        
        Args:
            new_headline: The new headline to publish.
            
        Returns:
            True if the headline was successfully published, False otherwise.
        """
        if not new_headline or not isinstance(new_headline, str):
            print("   -> Error: Invalid headline provided.")
            return False
            
        print(f"\n📰 PUBLISHER: New story released: '{new_headline}'")
        self._latest_headline = new_headline
        self.notify()  # <-- Critical: Automatically notifies Observers
        return True


# --- Demonstration of the Value ---
if __name__ == "__main__":
    print("\n--- ✅ Observer Demonstration (Efficient Push Notifications) ---")
    
    # 1. Initialize Components
    publisher = ObservableNewsPublisher()
    email_alert = NewsSubscriber("Email Alert Service")
    homepage_widget = NewsSubscriber("Homepage Widget")
    mobile_app = NewsSubscriber("Mobile App")
    
    # 2. Attach (Subscribe) the displays to the sensor
    publisher.attach(email_alert)
    publisher.attach(homepage_widget)
    publisher.attach(mobile_app)
    
    # 3. Simulate Publishing a Story
    # The publisher automatically notifies all subscribed components.
    publisher.publish_headline("Local Cat Rescued from Tree!")
    
    # 4. Detach one subscriber (e.g., the user turned off mobile alerts)
    publisher.detach(mobile_app)
    
    # 5. Simulate Another Story
    # Only the remaining attached subscribers are notified.
    publisher.publish_headline("Major City Council Decision Today.")
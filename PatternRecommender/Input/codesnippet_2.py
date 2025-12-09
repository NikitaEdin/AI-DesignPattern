

# --- 1. Abstract Observer (Subscriber Interface) ---
class Observer:
    """Interface for all News Subscribers."""
    def update(self, subject):
        raise NotImplementedError

# --- 2. Concrete Observer (Specific Subscribers) ---
class NewsSubscriber(Observer):
    """A subscriber that observes the news publisher."""
    def __init__(self, name):
        self.name = name

    def update(self, subject):
        # Observer is notified (pushed) with the new state (the headline)
        print(f"[{self.name} Subscriber] NOTIFIED! New Headline: {subject.get_headline()}")

# --- 3. Subject (News Publisher) ---
class ObservableNewsPublisher:
    """
    The Publisher class implemented as an Observable Subject.
    It manages a list of Observers (Subscribers).
    """
    def __init__(self):
        self._observers = []
        self._latest_headline = "No breaking news."

    def attach(self, observer):
        """Register a subscriber."""
        if observer not in self._observers:
            self._observers.append(observer)
        print(f"   -> {observer.name} is now attached (subscribed).")

    def detach(self, observer):
        """Unregister a subscriber."""
        try:
            self._observers.remove(observer)
            print(f"   -> {observer.name} is now detached (unsubscribed).")
        except ValueError:
            pass

    def notify(self):
        """Notify all attached observers of a change."""
        print("   -> NOTIFYING ALL SUBSCRIBERS...")
        for observer in self._observers:
            observer.update(self)

    def get_headline(self):
        return self._latest_headline

    def publish_headline(self, new_headline):
        """When a new story is published, all subscribers are notified."""
        print(f"\n📰 PUBLISHER: New story released: '{new_headline}'")
        self._latest_headline = new_headline
        self.notify() # <-- Critical: Automatically notifies Observers

# --- Demonstration of the Value ---

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
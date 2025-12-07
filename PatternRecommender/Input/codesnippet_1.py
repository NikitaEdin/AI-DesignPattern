### PATTERN 1: SINGLETON PUBLISHER ###

class SingletonNewsPublisher:
    """
    The News Publisher implemented as a Singleton.
    It guarantees a single point of truth for the news.
    """
    _instance = None
    _latest_headline = "No breaking news."

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonNewsPublisher, cls).__new__(cls)
        return cls._instance

    def get_headline(self):
        """Allows subscribers to retrieve the current headline."""
        return self._latest_headline

    def publish_headline(self, new_headline):
        """Updates the central headline but does not notify anyone."""
        print(f"\n PUBLISHER: Central headline updated to: '{new_headline}'")
        self._latest_headline = new_headline

class PollingSubscriber:
    """
    Subscriber component that connects to the single Publisher.
    It must check the Publisher whenever it needs an update.
    """
    def __init__(self, name):
        self.name = name
        # Subscriber connects to the single Publisher instance
        self.publisher = SingletonNewsPublisher()

    def check_for_news(self):
        """The subscriber actively PULLS the data from the Publisher."""
        current_headline = self.publisher.get_headline()
        print(f"[{self.name} Subscriber] PULLING NEWS... Current Headline: {current_headline}")

# --- Demonstration of the Singleton Method ---

print("--- 1 Singleton Publisher Demonstration (Pull Method) ---")

# 1. Initialize Components
the_bugle = SingletonNewsPublisher()
email_alert = PollingSubscriber("Email Alert Service")
homepage_widget = PollingSubscriber("Homepage Widget")

# 2. Simulate Publishing a Story
the_bugle.publish_headline("Local Cat Rescued from Tree!")

# 3. Subscribers manually pull the data
homepage_widget.check_for_news()
email_alert.check_for_news()

# 4. Simulate Another Story
the_bugle.publish_headline("Major City Council Decision Today.")

# 5. Subscribers must pull again to see the new news
homepage_widget.check_for_news()
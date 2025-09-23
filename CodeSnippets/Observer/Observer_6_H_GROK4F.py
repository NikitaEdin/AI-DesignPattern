class NewsFeed:
    def __init__(self):
        self._listeners = []
        self._message = ""

    def attach_listener(self, listener, priority=0):
        if any(l is listener for _, l in self._listeners):
            return
        self._listeners.append((priority, listener))
        self._listeners.sort(key=lambda x: x[0], reverse=True)

    def detach_listener(self, listener):
        self._listeners = [(p, l) for p, l in self._listeners if l != listener]

    def set_message(self, message):
        self._message = message
        self._notify()

    def _notify(self):
        notify_list = self._listeners[:]
        for priority, listener in notify_list:
            if any(l is listener for _, l in self._listeners):
                try:
                    listener.receive_update(self._message)
                except Exception:
                    self.detach_listener(listener)

class NewsOutlet:
    def __init__(self, name, priority=0):
        self.name = name
        self._priority = priority

    def receive_update(self, message):
        print(f"{self.name} (priority {self._priority}): {message}")

if __name__ == "__main__":
    feed = NewsFeed()
    outlet1 = NewsOutlet("Channel A", 1)
    outlet2 = NewsOutlet("Channel B", 2)
    outlet3 = NewsOutlet("Channel C", 1)

    feed.attach_listener(outlet2)
    feed.attach_listener(outlet1)
    feed.attach_listener(outlet3)
    feed.attach_listener(outlet2)  # duplicate, should ignore

    feed.set_message("Breaking news alert!")

    feed.detach_listener(outlet1)
    feed.set_message("Follow-up story.")

    # Simulate error in outlet3
    def faulty_update(msg):
        raise ValueError("Simulated error")
    outlet3.receive_update = faulty_update.__get__(outlet3)
    feed.attach_listener(outlet3, 3)
    feed.set_message("Emergency broadcast.")
import weakref

class DataSource:
    def __init__(self):
        self._subscribers = {}
        self._value = None

    def attach(self, subscriber, priority=0):
        if subscriber is None:
            return
        if id(subscriber) in self._subscribers:
            return
        self._subscribers[id(subscriber)] = (weakref.ref(subscriber), priority)

    def detach(self, subscriber):
        if subscriber is None:
            return
        key = id(subscriber)
        if key in self._subscribers:
            del self._subscribers[key]

    def set_value(self, value):
        self._value = value
        self._notify()

    def _notify(self):
        live_subscribers = []
        for key, (ref, priority) in list(self._subscribers.items()):
            sub = ref()
            if sub is not None:
                live_subscribers.append((priority, sub))
            else:
                del self._subscribers[key]
        live_subscribers.sort(key=lambda x: x[0], reverse=True)
        for _, sub in live_subscribers:
            try:
                sub.receive_update(self, self._value)
            except Exception:
                pass

    def get_value(self):
        return self._value

class DisplayPanel:
    def __init__(self, name, priority=0):
        self.name = name
        self.priority = priority

    def receive_update(self, source, value):
        print(f"{self.name} received: {value} from {source.get_value()}")

class NotificationService:
    def __init__(self, name, priority=10):
        self.name = name
        self.priority = priority

    def receive_update(self, source, value):
        if value > 100:
            print(f"{self.name} Alert: High value {value}!")
        else:
            print(f"{self.name} logged: {value}")

if __name__ == "__main__":
    source = DataSource()
    panel1 = DisplayPanel("Main Panel", priority=5)
    panel2 = DisplayPanel("Secondary Panel", priority=3)
    alert = NotificationService("High Alert Service")

    source.attach(panel1)
    source.attach(panel2)
    source.attach(alert)

    source.set_value(50)
    source.set_value(150)

    source.detach(panel2)
    source.set_value(75)

    del panel1
    source.set_value(200)
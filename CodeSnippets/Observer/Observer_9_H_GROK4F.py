import weakref
import threading

class Publisher:
    def __init__(self):
        self._dependents = []
        self._state = None
        self._lock = threading.Lock()

    def attach_dependent(self, dependent):
        with self._lock:
            self._dependents.append(weakref.ref(dependent))

    def detach_dependent(self, dependent):
        with self._lock:
            self._dependents = [ref for ref in self._dependents if ref() is dependent]

    def get_attachment_count(self):
        with self._lock:
            return len([ref for ref in self._dependents if ref() is not None])

    def update_state(self, new_state):
        self._state = new_state
        self._notify()

    def _notify(self):
        with self._lock:
            active_refs = [ref for ref in self._dependents if ref() is not None]
        for ref in active_refs:
            try:
                dependent = ref()
                if dependent:
                    dependent.update(self._state)
            except Exception:
                pass
        with self._lock:
            self._dependents = [ref for ref in self._dependents if ref() is not None]

class DataMonitor:
    def __init__(self, name):
        self.name = name
        self.last_state = None

    def update(self, state):
        self.last_state = state
        print(f"{self.name} received state update: {state}")

class AlertHandler:
    def __init__(self, threshold):
        self.threshold = threshold
        self.last_state = None

    def update(self, state):
        self.last_state = state
        if state > self.threshold:
            print(f"Alert: State {state} exceeds threshold {self.threshold}")

if __name__ == "__main__":
    pub = Publisher()
    mon1 = DataMonitor("Monitor1")
    mon2 = DataMonitor("Monitor2")
    alert = AlertHandler(50)

    pub.attach_dependent(mon1)
    pub.attach_dependent(mon2)
    pub.attach_dependent(alert)

    print(f"Initial attachments: {pub.get_attachment_count()}")
    pub.update_state(30)
    pub.update_state(60)

    pub.detach_dependent(mon1)
    print(f"After detachment: {pub.get_attachment_count()}")

    mon2 = None  # Simulate garbage collection
    import gc
    gc.collect()
    print(f"After cleanup: {pub.get_attachment_count()}")
    pub.update_state(70)
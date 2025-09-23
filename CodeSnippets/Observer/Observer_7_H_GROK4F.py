import weakref
import threading

class Publisher:
    def __init__(self):
        self._subscribers = []
        self._lock = threading.Lock()
        self._data = None
        self._data_changed = False

    def attach(self, subscriber):
        if subscriber not in [ref() for ref in self._subscribers if ref()]:
            with self._lock:
                self._subscribers.append(weakref.ref(subscriber, self._cleanup))
                self._data_changed = True

    def detach(self, subscriber):
        with self._lock:
            self._subscribers = [ref for ref in self._subscribers if ref() is not subscriber]
            self._data_changed = True

    def _cleanup(self, ref):
        with self._lock:
            if ref in self._subscribers:
                self._subscribers.remove(ref)
                self._data_changed = True

    def set_data(self, data):
        with self._lock:
            if self._data != data:
                self._data = data
                self._data_changed = True
        if self._data_changed:
            self._notify()

    def _notify(self):
        with self._lock:
            alive_subscribers = [ref() for ref in self._subscribers if ref() is not None]
            self._subscribers[:] = [weakref.ref(sub) for sub in alive_subscribers]
            self._data_changed = False
        for sub in alive_subscribers:
            try:
                sub.update(self._data)
            except Exception:
                pass

class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, data):
        print(f"{self.name} updated with data: {data}")

if __name__ == "__main__":
    pub = Publisher()
    sub1 = Subscriber("Subscriber A")
    sub2 = Subscriber("Subscriber B")
    sub3 = Subscriber("Subscriber C")

    pub.attach(sub1)
    pub.attach(sub2)
    pub.attach(sub3)

    pub.set_data("Initial Data")
    pub.set_data("Updated Data")

    pub.detach(sub2)

    pub.set_data("Final Data")

    import gc
    sub3 = None
    gc.collect()
    pub.set_data("Data After GC")
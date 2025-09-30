import threading
import time
import weakref
from typing import List, Optional

class Subject:
    def __init__(self):
        self._listeners = weakref.WeakSet()
        self._lock = threading.Lock()
    
    def attach(self, listener):
        with self._lock:
            self._listeners.add(listener)
    
    def detach(self, listener):
        with self._lock:
            self._listeners.discard(listener)
    
    def notify(self, event: str, data=None):
        with self._lock:
            refs = list(self._listeners)
        for listener in refs:
            try:
                listener.update(event, data)
            except Exception:
                pass

class Listener:
    def update(self, event: str, data=None):
        raise NotImplementedError

class Sensor(Subject):
    def __init__(self, threshold: float):
        super().__init__()
        self._threshold = threshold
        self._running = False
        self._reading = None
    
    def set_reading(self, value: float):
        if self._reading is None or abs(value - self._reading) >= self._threshold:
            self._reading = value
            self.notify('changed', value)

class Display(Listener):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, event: str, data=None):
        if event == 'changed':
            print(f'{self.name} updated: {data}')

class Logger(Listener):
    def __init__(self):
        self.history = []
    
    def update(self, event: str, data=None):
        self.history.append((time.time(), data))
    
    def get_last_n(self, n: int) -> List[float]:
        return [x[1] for x in self.history[-n:]]

if __name__ == '__main__':
    sensor = Sensor(0.5)
    display = Display('LCD')
    logger = Logger()
    sensor.attach(display)
    sensor.attach(logger)
    sensor.set_reading(10.0)
    sensor.set_reading(10.3)
    sensor.set_reading(10.4)
    sensor.detach(display)
    sensor.set_reading(11.0)
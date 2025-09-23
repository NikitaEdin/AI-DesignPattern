import weakref
from threading import Lock
from abc import ABC, abstractmethod

class UpdateListener(ABC):
    @abstractmethod
    def handle_update(self, data):
        pass

class SensorHub:
    def __init__(self):
        self._listeners = []
        self._lock = Lock()
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def attach(self, listener):
        with self._lock:
            if all(ref() is not listener for ref in self._listeners if ref() is not None):
                self._listeners.append(weakref.ref(listener))

    def detach(self, listener):
        with self._lock:
            self._listeners = [ref for ref in self._listeners if ref() is not listener and ref() is not None]

    def notify_listeners(self):
        with self._lock:
            active_listeners = [ref() for ref in self._listeners if ref() is not None]
        for listener in active_listeners:
            listener.handle_update({
                'temperature': self._temperature,
                'humidity': self._humidity,
                'pressure': self._pressure
            })

    def measurements_changed(self):
        self.notify_listeners()

    def set_measurements(self, temperature, humidity, pressure):
        if (temperature != self._temperature or
            humidity != self._humidity or
            pressure != self._pressure):
            self._temperature = temperature
            self._humidity = humidity
            self._pressure = pressure
            self.measurements_changed()

class CurrentConditions:
    def __init__(self, hub):
        self.hub = hub
        hub.attach(self)

    def handle_update(self, data):
        print(f"Current conditions: {data['temperature']}°C, {data['humidity']}% humidity")

    def __del__(self):
        self.hub.detach(self)

class StatisticsDisplay:
    def __init__(self, hub):
        self.hub = hub
        self.temperatures = []
        hub.attach(self)

    def handle_update(self, data):
        self.temperatures.append(data['temperature'])
        if self.temperatures:
            avg_temp = sum(self.temperatures) / len(self.temperatures)
            print(f"Statistics: Average temperature {avg_temp:.2f}°C")

    def __del__(self):
        self.hub.detach(self)

if __name__ == "__main__":
    hub = SensorHub()
    current = CurrentConditions(hub)
    stats = StatisticsDisplay(hub)
    hub.set_measurements(25.0, 65.0, 1013.1)
    hub.set_measurements(27.0, 70.0, 1012.0)
    del current
    hub.set_measurements(28.0, 75.0, 1011.0)
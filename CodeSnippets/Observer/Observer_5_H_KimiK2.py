import threading
from typing import List

class EventManager:
    def __init__(self) -> None:
        self._subscribers = {}
        self._lock = threading.Lock()
    
    def register(self, event_type: str, callback) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
    
    def unregister(self, event_type: str, callback) -> None:
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type].remove(callback)
    
    def notify(self, event_type: str, data) -> None:
        with self._lock:
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    callback(data)

class TemperatureSensor:
    def __init__(self) -> None:
        self._event_manager = EventManager()
        self._temperature = 0.0
        self._running = False
        self._thread = None
    
    def subscribe(self, callback) -> None:
        self._event_manager.register("temperature_change", callback)
    
    def unsubscribe(self, callback) -> None:
        self._event_manager.unregister("temperature_change", callback)
    
    def set_temperature(self, value: float) -> None:
        self._temperature = value
        self._event_manager.notify("temperature_change", value)
    
    def start_monitoring(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._monitor)
        self._thread.start()
    
    def stop_monitoring(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()
    
    def _monitor(self) -> None:
        import random
        import time
        while self._running:
            new_temp = random.uniform(20.0, 30.0)
            self.set_temperature(new_temp)
            time.sleep(1)

class TemperatureDisplay:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def update(self, value: float) -> None:
        print(f"{self.name}: Temperature is {value:.2f}°C")

class TemperatureAlert:
    def __init__(self) -> None:
        self.threshold = 27.0
    
    def check(self, value: float) -> None:
        if value > self.threshold:
            print(f"ALERT: High temperature detected: {value:.2f}°C")

if __name__ == "__main__":
    sensor = TemperatureSensor()
    display1 = TemperatureDisplay("Display 1")
    display2 = TemperatureDisplay("Display 2")
    alert = TemperatureAlert()
    
    sensor.subscribe(display1.update)
    sensor.subscribe(display2.update)
    sensor.subscribe(alert.check)
    
    sensor.start_monitoring()
    
    import time
    time.sleep(3)
    
    sensor.stop_monitoring()
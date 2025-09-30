import threading
import random
import time


class SensorWatcher:
    def __init__(self):
        self._active = True

    def update(self, sensor, temperature, display):
        raise NotImplementedError

    def deactivate(self):
        self._active = False

    def is_active(self):
        return self._active


class ConsoleLogger(SensorWatcher):
    def update(self, sensor, temperature, display):
        if self.is_active():
            print(f"[Console] Sensor {sensor.name}: {temperature}°C")


class ScreenDisplay(SensorWatcher):
    def update(self, sensor, temperature, display):
        if self.is_active() and display:
            print(f"[Screen] Alert: {sensor.name} reached {temperature}°C")


class Sensor:
    def __init__(self, name, threshold=30):
        self.name = name
        self.temperature = 20
        self.threshold = threshold
        self._watchers = []
        self._lock = threading.Lock()

    def add_watcher(self, watcher):
        with self._lock:
            self._watchers.append(watcher)

    def remove_watcher(self, watcher):
        with self._lock:
            try:
                self._watchers.remove(watcher)
            except ValueError:
                pass

    def notify_watchers(self, display=True):
        with self._lock:
            watchers_copy = [w for w in self._watchers if w.is_active()]
        for watcher in watchers_copy:
            watcher.update(self, self.temperature, display)

    def simulate(self):
        while True:
            delta = random.uniform(-5, 5)
            with self._lock:
                self.temperature += delta
                self.temperature = max(10, min(50, self.temperature))
                if self.temperature > self.threshold:
                    self.notify_watchers(display=True)
                else:
                    self.notify_watchers(display=False)
            time.sleep(random.uniform(0.5, 1.5))


def main():
    sensor = Sensor("Living Room", threshold=28)
    console = ConsoleLogger()
    screen = ScreenDisplay()
    sensor.add_watcher(console)
    sensor.add_watcher(screen)

    thread = threading.Thread(target=sensor.simulate, daemon=True)
    thread.start()

    time.sleep(10)
    screen.deactivate()
    time.sleep(5)


if __name__ == "__main__":
    main()
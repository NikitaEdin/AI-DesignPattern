class Publisher:
    def __init__(self):
        self._watchers = []

    def attach(self, watcher):
        self._watchers.append(watcher)

    def detach(self, watcher):
        self._watchers.remove(watcher)

    def notify(self, data):
        for watcher in self._watchers:
            watcher.update(data)


class TempWatcher:
    def update(self, data):
        if data > 25:
            print(f"High temperature alert: {data}°C")


class FanController:
    def __init__(self):
        self.is_on = False

    def update(self, data):
        if data > 22 and not self.is_on:
            print("Fan activated.")
            self.is_on = True
        elif data <= 22 and self.is_on:
            print("Fan deactivated.")
            self.is_on = False


class TemperatureGauge(Publisher):
    def __init__(self):
        super().__init__()
        self._temp = 0

    def set_temperature(self, temp):
        self._temp = temp
        self.notify(temp)


if __name__ == "__main__":
    gauge = TemperatureGauge()
    temp_watcher = TempWatcher()
    fan = FanController()

    gauge.attach(temp_watcher)
    gauge.attach(fan)

    gauge.set_temperature(24)
    gauge.set_temperature(26)
    gauge.set_temperature(21)
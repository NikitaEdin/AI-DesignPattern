class WeatherStation:
    def __init__(self):
        self._temperature = 0.0
        self._subscribers = []
        self._logger = []

    def register_subscriber(self, subscriber):
        if not hasattr(subscriber, 'update_temperature'):
            raise ValueError("Subscriber must have update_temperature method")
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
            self._log_event(f"Registered {subscriber._name}")

    def remove_subscriber(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
            self._log_event(f"Removed {subscriber._name}")

    def set_temperature(self, temperature):
        if not isinstance(temperature, (int, float)):
            raise ValueError("Temperature must be a number")
        self._temperature = temperature
        self.notify_subscribers()

    def notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber.update_temperature(self._temperature)
        self._log_event(f"Notified {len(self._subscribers)} subscribers of temperature {self._temperature}")

    def _log_event(self, event):
        self._logger.append(event)
        print(f"Log: {event}")

    def get_logs(self):
        return self._logger

class ThermometerDisplay:
    def __init__(self, name):
        self._name = name

    def update_temperature(self, temperature):
        print(f"{self._name} display updated: Current temperature is {temperature}°C")

if __name__ == "__main__":
    station = WeatherStation()
    display1 = ThermometerDisplay("Living Room")
    display2 = ThermometerDisplay("Kitchen")

    station.register_subscriber(display1)
    station.register_subscriber(display2)
    station.set_temperature(22.5)

    station.remove_subscriber(display1)
    station.set_temperature(25.0)

    print("\nRecent logs:")
    for log in station.get_logs():
        print(log)
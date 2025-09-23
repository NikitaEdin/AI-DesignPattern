class DataProvider:
    def __init__(self):
        self._listeners = []
        self._data = None

    def attach(self, listener):
        self._listeners.append(listener)

    def detach(self, listener):
        self._listeners.remove(listener)

    def notify(self):
        for listener in self._listeners:
            listener.update(self._data)

    def set_data(self, data):
        self._data = data
        self.notify()

class Display:
    def update(self, data):
        pass

class CurrentDisplay(Display):
    def update(self, data):
        print(f"Current conditions: {data}")

if __name__ == "__main__":
    station = DataProvider()
    display = CurrentDisplay()
    station.attach(display)
    station.set_data("Sunny, 75°F")
    station.set_data("Cloudy, 65°F")
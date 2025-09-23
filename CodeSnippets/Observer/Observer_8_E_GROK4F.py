class DataSource:
    def __init__(self):
        self._displays = []
        self._data = 0

    def attach(self, display):
        self._displays.append(display)

    def detach(self, display):
        self._displays.remove(display)

    def set_data(self, value):
        self._data = value
        self.notify()

    def notify(self):
        for display in self._displays:
            display.update(self._data)

class Display:
    def update(self, data):
        print(f"Received data: {data}")

if __name__ == "__main__":
    source = DataSource()
    d1 = Display()
    d2 = Display()
    source.attach(d1)
    source.attach(d2)
    source.set_data(42)
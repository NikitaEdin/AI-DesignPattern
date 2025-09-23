class WeatherStation:
    def __init__(self):
        self._temperature = 0
        self._displays = []

    def attach(self, display):
        self._displays.append(display)

    def set_temperature(self, temp):
        self._temperature = temp
        self._notify()

    def _notify(self):
        for display in self._displays:
            display.update(self._temperature)

class CurrentConditionsDisplay:
    def update(self, temperature):
        print(f"Current temperature: {temperature}°C")

if __name__ == "__main__":
    station = WeatherStation()
    display = CurrentConditionsDisplay()
    station.attach(display)
    station.set_temperature(25)
    station.set_temperature(30)
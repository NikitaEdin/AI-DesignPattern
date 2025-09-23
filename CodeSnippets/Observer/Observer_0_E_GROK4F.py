class WeatherStation:
    def __init__(self):
        self._displays = []
        self._temperature = 0

    def register_display(self, display):
        self._displays.append(display)

    def remove_display(self, display):
        self._displays.remove(display)

    def notify_displays(self):
        for display in self._displays:
            display.update_temperature(self._temperature)

    def set_temperature(self, temp):
        self._temperature = temp
        self.notify_displays()

class CurrentDisplay:
    def update_temperature(self, temp):
        print(f"Current temperature: {temp}")

if __name__ == "__main__":
    station = WeatherStation()
    display1 = CurrentDisplay()
    display2 = CurrentDisplay()
    station.register_display(display1)
    station.register_display(display2)
    station.set_temperature(25)
    station.set_temperature(30)
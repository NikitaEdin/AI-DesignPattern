class WeatherData:
    def __init__(self):
        self._temperature = 0.0
        self._humidity = 0.0
        self._displays = []

    def register_display(self, display):
        self._displays.append(display)

    def remove_display(self, display):
        self._displays.remove(display)

    def notify_displays(self):
        for display in self._displays:
            display.update(self)

    def measurements_changed(self):
        self.notify_displays()

    def set_measurements(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        self.measurements_changed()

    def get_temperature(self):
        return self._temperature

    def get_humidity(self):
        return self._humidity

class CurrentConditionsDisplay:
    def __init__(self, weather_data):
        self._weather_data = weather_data
        weather_data.register_display(self)

    def update(self, weather_data):
        self._temperature = weather_data.get_temperature()
        self._humidity = weather_data.get_humidity()
        print(f"Current conditions: {self._temperature}F degrees and {self._humidity}% humidity")

class StatisticsDisplay:
    def __init__(self, weather_data):
        self._weather_data = weather_data
        weather_data.register_display(self)

    def update(self, weather_data):
        temp = weather_data.get_temperature()
        hum = weather_data.get_humidity()
        print(f"Statistics: avg temp {temp:.1f}F, avg humidity {hum:.1f}%")

if __name__ == "__main__":
    weather_data = WeatherData()
    current_display = CurrentConditionsDisplay(weather_data)
    stats_display = StatisticsDisplay(weather_data)
    weather_data.set_measurements(80.0, 65.0)
    weather_data.set_measurements(82.0, 70.0)
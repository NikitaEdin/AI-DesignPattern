class WeatherData:
    def __init__(self):
        self._temperature = 0.0
        self._humidity = 0.0
        self._displays = []

    def register_display(self, display):
        if display not in self._displays:
            self._displays.append(display)

    def remove_display(self, display):
        if display in self._displays:
            self._displays.remove(display)

    def notify_displays(self):
        if not self._displays:
            return
        for display in self._displays:
            display.update(self._temperature, self._humidity)

    def measurements_changed(self):
        self.notify_displays()

    def set_measurements(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        self.measurements_changed()

class CurrentConditionsDisplay:
    def __init__(self, weather_data):
        self._weather_data = weather_data
        self._temperature = 0.0
        self._humidity = 0.0
        weather_data.register_display(self)

    def update(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        self.display()

    def display(self):
        print(f"Current conditions: {self._temperature}°C and {self._humidity}% humidity")

class StatisticsDisplay:
    def __init__(self, weather_data):
        self._weather_data = weather_data
        self._temp_sum = 0.0
        self._humidity_sum = 0.0
        self._count = 0
        weather_data.register_display(self)

    def update(self, temperature, humidity):
        self._temp_sum += temperature
        self._humidity_sum += humidity
        self._count += 1
        self.display()

    def display(self):
        avg_temp = self._temp_sum / self._count
        avg_hum = self._humidity_sum / self._count
        print(f"Average conditions: {avg_temp:.1f}°C and {avg_hum:.1f}% humidity")

if __name__ == "__main__":
    weather_data = WeatherData()
    current_display = CurrentConditionsDisplay(weather_data)
    stats_display = StatisticsDisplay(weather_data)
    
    weather_data.set_measurements(25.0, 65.0)
    weather_data.set_measurements(28.0, 70.0)
    
    weather_data.remove_display(stats_display)
    weather_data.set_measurements(22.0, 55.0)
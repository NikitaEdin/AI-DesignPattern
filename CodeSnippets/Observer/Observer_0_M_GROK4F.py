class WeatherData:
    def __init__(self):
        self.displays = []
        self.temperature = 0.0
        self.humidity = 0.0

    def register_display(self, display):
        if display not in self.displays:
            self.displays.append(display)

    def remove_display(self, display):
        if display in self.displays:
            self.displays.remove(display)

    def notify_displays(self):
        for display in self.displays:
            display.update(self.temperature, self.humidity)

    def measurements_changed(self):
        self.notify_displays()

    def set_measurements(self, temp, hum):
        self.temperature = temp
        self.humidity = hum
        self.measurements_changed()

class CurrentDisplay:
    def __init__(self):
        self.temperature = 0.0
        self.humidity = 0.0

    def update(self, temp, hum):
        self.temperature = temp
        self.humidity = hum
        self.show()

    def show(self):
        print(f"Current conditions: {self.temperature}°C and {self.humidity}% humidity")

class StatsDisplay:
    def __init__(self):
        self.temp_sum = 0.0
        self.num_readings = 0

    def update(self, temp, hum):
        self.temp_sum += temp
        self.num_readings += 1
        self.show()

    def show(self):
        if self.num_readings > 0:
            avg = self.temp_sum / self.num_readings
            print(f"Average temperature: {avg:.2f}°C")

if __name__ == "__main__":
    weather_data = WeatherData()
    current_display = CurrentDisplay()
    stats_display = StatsDisplay()
    weather_data.register_display(current_display)
    weather_data.register_display(stats_display)
    weather_data.set_measurements(25.0, 65.0)
    weather_data.set_measurements(27.0, 70.0)
    weather_data.remove_display(current_display)
    weather_data.set_measurements(30.0, 75.0)
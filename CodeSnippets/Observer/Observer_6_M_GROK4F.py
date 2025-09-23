class WeatherStation:
    def __init__(self):
        self.displays = []
        self.temperature = 0.0
        self.humidity = 0.0

    def register_display(self, display):
        if display not in self.displays:
            self.displays.append(display)
        else:
            raise ValueError("Display already registered")

    def unregister_display(self, display):
        if display in self.displays:
            self.displays.remove(display)
        else:
            raise ValueError("Display not registered")

    def measurements_changed(self):
        for display in self.displays:
            display.update(self.temperature, self.humidity)

    def set_measurements(self, temp, hum):
        self.temperature = temp
        self.humidity = hum
        self.measurements_changed()

class CurrentConditionsDisplay:
    def __init__(self, station):
        self.station = station
        self.temp = 0.0
        self.hum = 0.0
        station.register_display(self)

    def update(self, temp, hum):
        self.temp = temp
        self.hum = hum
        self.display_current()

    def display_current(self):
        print(f"Current conditions: {self.temp}°C and {self.hum}% humidity")

class StatisticsDisplay:
    def __init__(self, station):
        self.station = station
        self.max_temp = 0.0
        self.min_temp = 200.0
        self.temp_sum = 0.0
        self.num_readings = 0
        station.register_display(self)

    def update(self, temp, hum):
        self.temp_sum += temp
        self.num_readings += 1
        if temp > self.max_temp:
            self.max_temp = temp
        if temp < self.min_temp:
            self.min_temp = temp
        self.display_stats()

    def display_stats(self):
        avg_temp = self.temp_sum / self.num_readings if self.num_readings > 0 else 0
        print(f"Avg/Max/Min Temperature: {avg_temp:.1f}°C / {self.max_temp}°C / {self.min_temp}°C")

if __name__ == "__main__":
    station = WeatherStation()
    current_display = CurrentConditionsDisplay(station)
    stats_display = StatisticsDisplay(station)
    station.set_measurements(25.0, 65.0)
    station.set_measurements(28.0, 70.0)
    station.unregister_display(current_display)
    station.set_measurements(30.0, 75.0)
class WeatherData:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, weather):
        for observer in self.observers:
            observer.update(weather)

class WeatherStation:
    def __init__(self):
        self.data = WeatherData()

    def set_temperature(self, temperature):
        self.data.set_temperature(temperature)

    def set_humidity(self, humidity):
        self.data.set_humidity(humidity)

class CurrentWeatherDisplay:
    def __init__(self):
        self.data = WeatherData()

    def update(self, weather):
        print("Current conditions:", weather.temperature, weather.humidity)

class StatisticsLogger:
    def __init__(self):
        self.data = WeatherData()

    def update(self, weather):
        print("Temperature:", weather.temperature)

if __name__ == "__main__":
    weather_station = WeatherStation()
    current_weather_display = CurrentWeatherDisplay()
    statistics_logger = StatisticsLogger()

    weather_station.data.register_observer(current_weather_display)
    weather_station.data.register_observer(statistics_logger)

    for i in range(10):
        weather_station.set_temperature(20 + i)
        weather_station.set_humidity(60 + i)

    weather_station.data.remove_observer(current_weather_display)

    for i in range(10, 20):
        weather_station.set_temperature(i)
        weather_station.set_humidity(60 + i)
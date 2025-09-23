class CelsiusThermometer:
    def get_temperature(self) -> float:
        pass

class FahrenheitWeatherReader:
    def read_temperature(self) -> float:
        return 68.0

class UnifiedTemperatureReader(CelsiusThermometer):
    def __init__(self, weather_reader: FahrenheitWeatherReader):
        self.weather_reader = weather_reader

    def get_temperature(self) -> float:
        f = self.weather_reader.read_temperature()
        if not isinstance(f, (int, float)) or f < -459.67:
            raise ValueError("Invalid temperature reading from weather service.")
        return (f - 32) * 5.0 / 9.0

class WeatherApp:
    def __init__(self, thermometer: CelsiusThermometer):
        self.thermometer = thermometer

    def show_current_temp(self) -> None:
        try:
            temp = self.thermometer.get_temperature()
            print(f"The current temperature is {temp:.1f}°C")
        except ValueError as e:
            print(f"Error reading temperature: {e}")

if __name__ == "__main__":
    legacy_reader = FahrenheitWeatherReader()
    modern_thermometer = UnifiedTemperatureReader(legacy_reader)
    application = WeatherApp(modern_thermometer)
    application.show_current_temp()
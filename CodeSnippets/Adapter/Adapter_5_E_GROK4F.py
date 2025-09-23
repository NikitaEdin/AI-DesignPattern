class TemperatureReader:
    def get_temperature(self):
        pass

class CelsiusSensor:
    def get_celsius(self):
        return 25.0

class FahrenheitSensor:
    def __init__(self, sensor):
        self.sensor = sensor

    def get_temperature(self):
        celsius = self.sensor.get_celsius()
        return (celsius * 9 / 5) + 32

class Display:
    def __init__(self, reader):
        self.reader = reader

    def show(self):
        temp = self.reader.get_temperature()
        print(f"Current temperature: {temp:.1f}°F")

if __name__ == "__main__":
    sensor = CelsiusSensor()
    converter = FahrenheitSensor(sensor)
    display = Display(converter)
    display.show()
import random

class OldFahrenheitReader:
    def get_fahrenheit(self) -> float:
        return random.uniform(32, 212)

class CelsiusCompatibleReader:
    def __init__(self, old_reader):
        if not isinstance(old_reader, OldFahrenheitReader):
            raise TypeError("Must provide an OldFahrenheitReader instance")
        self.old_reader = old_reader

    def get_temperature_in_celsius(self) -> float:
        f = self.old_reader.get_fahrenheit()
        c = (f - 32) * 5 / 9
        if c < -273:
            raise ValueError("Temperature below absolute zero")
        return c

class DirectCelsiusReader:
    def get_temperature_in_celsius(self) -> float:
        return random.uniform(-50, 50)

if __name__ == "__main__":
    old_reader = OldFahrenheitReader()
    adapted_reader = CelsiusCompatibleReader(old_reader)
    direct_reader = DirectCelsiusReader()

    readers = [adapted_reader, direct_reader]

    for reader in readers:
        try:
            temp = reader.get_temperature_in_celsius()
            print(f"Current temperature: {temp:.2f}°C")
        except ValueError as e:
            print(f"Measurement error: {e}")
class Subject:
    def __init__(self) -> None:
        self._observers = set()
    
    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update()

class Observer:
    def __init__(self, subject: Subject) -> None:
        self._subject = subject
        self._subject.attach(self)
    
    def update(self) -> None:
        pass

class WeatherData:
    def __init__(self) -> None:
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0
    
    def measurementsChanged(self, temperature: float, humidity: float, pressure: float) -> None:
        if self._temperature != temperature or self._humidity != humidity or self._pressure != pressure:
            self._temperature = temperature
            self._humidity = humidity
            self._pressure = pressure
            self._subject.notify()

if __name__ == "__main__":
    weather_data = WeatherData()
    current_conditions_display = CurrentConditionsDisplay(weather_data)
    statistics_display = StatisticsDisplay(weather_data)
    forecast_display = ForecastDisplay(weather_data)
    
    for i in range(10):
        temperature = random.randint(20, 35)
        humidity = random.randint(40, 60)
        pressure = random.randint(80, 110)
        weather_data.measurementsChanged(temperature, humidity, pressure)
    
    current_conditions_display.display()
    statistics_display.display()
    forecast_display.display()
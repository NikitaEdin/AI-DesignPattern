from __future__ import annotations
from abc import ABC, abstractmethod
import json
from typing import Any

class ExternalWeatherAPI:
    def fetch_raw(self, endpoint: str) -> dict[str, Any]:
        return {"temp": 22.5, "humidity": 78, "wind": "5km/h"}

class ExternalWeatherService:
    def get_weather(self, location: str) -> str:
        raw = ExternalWeatherAPI().fetch_raw(location)
        return json.dumps({"temperature_c": raw["temp"], "humidity_pct": raw["humidity"], "wind_kmh": raw["wind"]})

class WeatherClientInterface(ABC):
    @abstractmethod
    def retrieve_temperature(self, location: str) -> float: ...
    
    @abstractmethod
    def retrieve_humidity(self, location: str) -> int: ...

class UnifiedWeatherBridge(WeatherClientInterface):
    def __init__(self, service: ExternalWeatherService) -> None:
        self._service = service
    
    def retrieve_temperature(self, location: str) -> float:
        payload = json.loads(self._service.get_weather(location))
        return float(payload["temperature_c"])
    
    def retrieve_humidity(self, location: str) -> int:
        payload = json.loads(self._service.get_weather(location))
        return int(payload["humidity_pct"])

class LocalWeatherMonitor:
    def __init__(self, client: WeatherClientInterface) -> None:
        self._client = client
    
    def report(self, location: str) -> str:
        temp = self._client.retrieve_temperature(location)
        humidity = self._client.retrieve_humidity(location)
        return f"Location {location}: {temp}°C, {humidity}% humidity"

if __name__ == "__main__":
    legacy = ExternalWeatherService()
    bridge = UnifiedWeatherBridge(legacy)
    monitor = LocalWeatherMonitor(bridge)
    print(monitor.report("Berlin"))
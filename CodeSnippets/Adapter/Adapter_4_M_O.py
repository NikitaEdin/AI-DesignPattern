import time
import random
from abc import ABC, abstractmethod
from typing import Optional


class TemperatureSource(ABC):
    @abstractmethod
    def read_celsius(self) -> float:
        pass


class LegacyTempSensor:
    def __init__(self, failure_chance: float = 0.1):
        self.failure_chance = max(0.0, min(1.0, failure_chance))

    def get_temperature_fahrenheit(self) -> float:
        if random.random() < self.failure_chance:
            raise RuntimeError("legacy sensor failure")
        return 68.0 + random.uniform(-5.0, 5.0)


class ReadError(Exception):
    pass


class SensorBridge(TemperatureSource):
    def __init__(self, legacy: LegacyTempSensor, cache_ttl: float = 1.0, fallback_celsius: Optional[float] = None):
        self._legacy = legacy
        self._cache_ttl = max(0.0, cache_ttl)
        self._fallback = fallback_celsius
        self._last_value: Optional[float] = None
        self._last_time: float = 0.0

    def _f_to_c(self, f: float) -> float:
        return (f - 32.0) * 5.0 / 9.0

    def read_celsius(self) -> float:
        now = time.time()
        if self._last_value is not None and (now - self._last_time) <= self._cache_ttl:
            return self._last_value
        try:
            f = self._legacy.get_temperature_fahrenheit()
            c = self._f_to_c(f)
            self._last_value = c
            self._last_time = now
            return c
        except Exception as exc:
            if self._fallback is not None:
                if self._last_value is None:
                    self._last_value = self._fallback
                    self._last_time = now
                return self._last_value
            raise ReadError("unable to read from sensor") from exc


if __name__ == "__main__":
    random.seed(42)
    legacy = LegacyTempSensor(failure_chance=0.3)
    bridge = SensorBridge(legacy, cache_ttl=0.5, fallback_celsius=20.0)
    for i in range(10):
        try:
            temp = bridge.read_celsius()
            print(f"Reading {i+1}: {temp:.2f} °C")
        except ReadError as e:
            print(f"Reading {i+1}: error - {e}")
        time.sleep(0.2)
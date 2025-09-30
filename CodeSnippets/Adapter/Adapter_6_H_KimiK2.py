from typing import Protocol, runtime_checkable
import asyncio
from abc import ABC, abstractmethod


@runtime_checkable
class Sensor(Protocol):
    def read_sync(self) -> float: ...


class TemperatureSource:
    async def fetch(self) -> float:
        await asyncio.sleep(0.1)
        return 22.3


class HumidityInterface:
    def __init__(self, factor: float = 1.0):
        self.factor = factor

    def get_value(self) -> float:
        return 55.7 * self.factor


class MultiSource:
    def __init__(self, raw: float):
        self._raw = raw

    async def pull_value(self) -> float:
        await asyncio.sleep(0.05)
        return self._raw


class SyncBridge:
    def __init__(self, source):
        self.source = source

    def read_sync(self) -> float:
        return asyncio.run(self._async_read())

    async def _async_read(self) -> float:
        try:
            return await self.source.fetch()
        except AttributeError:
            return await self.source.pull_value()


class HumidityBridge:
    def __init__(self, sensor: HumidityInterface):
        self.sensor = sensor

    def read_sync(self) -> float:
        return self.sensor.get_value()


def main():
    async_source = TemperatureSource()
    sync_sensor = SyncBridge(async_source)
    print(sync_sensor.read_sync())

    humidity = HumidityInterface(0.9)
    humidity_sensor = HumidityBridge(humidity)
    print(humidity_sensor.read_sync())

    multi = MultiSource(30.0)
    multi_sensor = SyncBridge(multi)
    print(multi_sensor.read_sync())


if __name__ == "__main__":
    main()
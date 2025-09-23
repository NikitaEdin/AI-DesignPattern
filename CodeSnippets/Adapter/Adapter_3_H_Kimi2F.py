import abc
from typing import Protocol, runtime_checkable
import asyncio


@runtime_checkable
class EuropeanSocket(Protocol):
    def provide_230v(self) -> int:
        ...


class UKSocket:
    def give_240v(self) -> int:
        return 240


class USSocket:
    def give_120v(self) -> int:
        return 120


class PowerBridge:
    def __init__(self, socket: EuropeanSocket):
        self._socket = socket

    def use_device(self) -> None:
        volts = self._socket.provide_230v()
        if volts != 230:
            raise ValueError("Incompatible voltage")
        print(f"Device running on {volts}V")


class UKToEuropeanWrapper(EuropeanSocket):
    def __init__(self, uk: UKSocket):
        self._uk = uk

    def provide_230v(self) -> int:
        v = self._uk.give_240v()
        if v != 240:
            raise ValueError("Unexpected UK voltage")
        return 230


class USToEuropeanWrapper(EuropeanSocket):
    def __init__(self, us: USSocket):
        self._us = us

    def provide_230v(self) -> int:
        v = self._us.give_120v()
        if v != 120:
            raise ValueError("Unexpected US voltage")
        return 230


async def main():
    uk = UKSocket()
    us = USSocket()

    bridge1 = PowerBridge(UKToEuropeanWrapper(uk))
    bridge2 = PowerBridge(USToEuropeanWrapper(us))

    bridge1.use_device()
    bridge2.use_device()


if __name__ == "__main__":
    asyncio.run(main())
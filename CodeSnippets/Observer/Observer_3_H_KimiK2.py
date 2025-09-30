import asyncio
from typing import List, Callable, Optional, Any
from contextlib import suppress

class EventStream:
    def __init__(self) -> None:
        self._subscribers: List[Callable[[Any], None]] = []
        self._is_frozen: bool = False

    def subscribe(self, callback: Callable[[Any], None]) -> 'Subscription':
        if self._is_frozen:
            raise RuntimeError("Stream frozen")
        self._subscribers.append(callback)
        return Subscription(self, callback)

    def emit(self, data: Any) -> None:
        if self._is_frozen:
            raise RuntimeError("Stream frozen")
        for callback in self._subscribers.copy():
            with suppress(Exception):
                callback(data)

    def freeze(self) -> None:
        self._is_frozen = True

class Subscription:
    def __init__(self, stream: EventStream, callback: Callable[[Any], None]) -> None:
        self._stream = stream
        self._callback = callback

    def close(self) -> None:
        with suppress(ValueError):
            self._stream._subscribers.remove(self._callback)

class StockTicker(EventStream):
    def __init__(self) -> None:
        super().__init__()
        self._price: float = 0.0
        self._threshold: Optional[float] = None

    @property
    def price(self) -> float:
        return self._price

    def update_price(self, new_price: float) -> None:
        self._price = new_price
        self.emit(new_price)

    def set_threshold(self, threshold: float) -> None:
        self._threshold = threshold

    def emit(self, data: Any) -> None:
        if self._threshold is not None and data < self._threshold:
            return
        super().emit(data)

async def main() -> None:
    ticker = StockTicker()
    sub1 = ticker.subscribe(lambda p: print(f"Alert A: {p}"))
    sub2 = ticker.subscribe(lambda p: print(f"Alert B: {p}") if p > 200 else None)
    ticker.set_threshold(100)

    for price in (95, 150, 220):
        ticker.update_price(price)
        await asyncio.sleep(0.1)

    sub1.close()
    ticker.freeze()
    ticker.update_price(300)

if __name__ == "__main__":
    asyncio.run(main())
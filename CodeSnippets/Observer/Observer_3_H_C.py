import weakref
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from functools import wraps

class Subscriber(ABC):
    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._subscribers: List[weakref.ref] = []
        self._filtered_subscribers: Dict[str, List[weakref.ref]] = {}

    def subscribe(self, subscriber: Subscriber, event_filter: Optional[str] = None) -> None:
        ref = weakref.ref(subscriber, self._cleanup_subscriber)
        if event_filter:
            if event_filter not in self._filtered_subscribers:
                self._filtered_subscribers[event_filter] = []
            self._filtered_subscribers[event_filter].append(ref)
        else:
            self._subscribers.append(ref)

    def unsubscribe(self, subscriber: Subscriber) -> None:
        self._subscribers = [ref for ref in self._subscribers if ref() is not subscriber]
        for event_type, refs in self._filtered_subscribers.items():
            self._filtered_subscribers[event_type] = [ref for ref in refs if ref() is not subscriber]

    def notify(self, event: str, data: Any) -> None:
        all_refs = self._subscribers + self._filtered_subscribers.get(event, [])
        for ref in all_refs[:]:
            subscriber = ref()
            if subscriber:
                try:
                    subscriber.update(event, data)
                except Exception as e:
                    print(f"Notification error: {e}")

    def _cleanup_subscriber(self, ref):
        if ref in self._subscribers:
            self._subscribers.remove(ref)
        for refs in self._filtered_subscribers.values():
            if ref in refs:
                refs.remove(ref)

def event_listener(publisher: Publisher, event_filter: Optional[str] = None):
    def decorator(cls):
        original_init = cls.__init__
        
        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            publisher.subscribe(self, event_filter)
        
        cls.__init__ = new_init
        return cls
    return decorator

class StockMarket(Publisher):
    def __init__(self):
        super().__init__()
        self.prices = {}

    def update_price(self, symbol: str, price: float):
        old_price = self.prices.get(symbol, price)
        self.prices[symbol] = price
        change = ((price - old_price) / old_price * 100) if old_price else 0
        self.notify("price_change", {"symbol": symbol, "price": price, "change": change})

class TradingBot(Subscriber):
    def __init__(self, name: str):
        self.name = name
        self.portfolio = {}

    def update(self, event: str, data: Any) -> None:
        symbol = data["symbol"]
        price = data["price"]
        change = data["change"]
        
        if change > 5:
            print(f"{self.name}: Selling {symbol} at ${price:.2f} (+{change:.1f}%)")
        elif change < -5:
            print(f"{self.name}: Buying {symbol} at ${price:.2f} ({change:.1f}%)")

@event_listener(StockMarket(), "price_change")
class PriceTracker(Subscriber):
    def __init__(self, tracked_symbols: List[str]):
        self.tracked_symbols = tracked_symbols
        self.history = {}

    def update(self, event: str, data: Any) -> None:
        symbol = data["symbol"]
        if symbol in self.tracked_symbols:
            price = data["price"]
            if symbol not in self.history:
                self.history[symbol] = []
            self.history[symbol].append(price)
            print(f"Tracker: {symbol} price history: {self.history[symbol][-3:]}")

if __name__ == "__main__":
    market = StockMarket()
    
    bot1 = TradingBot("AlgoBot")
    bot2 = TradingBot("QuickTrade")
    tracker = PriceTracker(['AAPL', 'GOOGL', 'MSFT'])
    
    market.subscribe(bot1)
    market.subscribe(bot2)
    
    market.update_price("AAPL", 150.0)
    market.update_price("AAPL", 158.0)
    market.update_price("GOOGL", 2800.0)
    market.update_price("MSFT", 300.0)
    market.update_price("AAPL", 140.0)
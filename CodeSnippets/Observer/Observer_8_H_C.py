from typing import Protocol, Set, Any, Dict
from weakref import WeakSet
import threading
from functools import wraps

class Subscriber(Protocol):
    def notify(self, event_type: str, data: Any) -> None: ...

def thread_safe(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)
    return wrapper

class Publisher:
    def __init__(self):
        self._subscribers: Dict[str, WeakSet] = {}
        self._lock = threading.RLock()
    
    @thread_safe
    def subscribe(self, subscriber: Subscriber, event_type: str = "default") -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = WeakSet()
        self._subscribers[event_type].add(subscriber)
    
    @thread_safe
    def unsubscribe(self, subscriber: Subscriber, event_type: str = "default") -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type].discard(subscriber)
    
    @thread_safe
    def broadcast(self, event_type: str = "default", data: Any = None) -> None:
        if event_type in self._subscribers:
            dead_refs = []
            for subscriber in self._subscribers[event_type].copy():
                try:
                    subscriber.notify(event_type, data)
                except ReferenceError:
                    dead_refs.append(subscriber)
            for ref in dead_refs:
                self._subscribers[event_type].discard(ref)

class StockTicker(Publisher):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol
        self._price = 0.0
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value: float):
        old_price = self._price
        self._price = value
        change = value - old_price
        
        self.broadcast("price_update", {"symbol": self.symbol, "price": value, "change": change})
        
        if change > 0:
            self.broadcast("price_increase", {"symbol": self.symbol, "price": value, "change": change})
        elif change < 0:
            self.broadcast("price_decrease", {"symbol": self.symbol, "price": value, "change": change})

class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.total_value = 0.0
    
    def notify(self, event_type: str, data: Any) -> None:
        if event_type == "price_update":
            print(f"Portfolio '{self.name}': {data['symbol']} updated to ${data['price']:.2f}")

class AlertSystem:
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def notify(self, event_type: str, data: Any) -> None:
        if event_type == "price_increase" and abs(data['change']) >= self.threshold:
            print(f"ALERT: {data['symbol']} surged by ${data['change']:.2f} to ${data['price']:.2f}")
        elif event_type == "price_decrease" and abs(data['change']) >= self.threshold:
            print(f"ALERT: {data['symbol']} dropped by ${abs(data['change']):.2f} to ${data['price']:.2f}")

if __name__ == "__main__":
    ticker = StockTicker("AAPL")
    
    portfolio1 = Portfolio("Tech Fund")
    portfolio2 = Portfolio("Growth Fund")
    alert_system = AlertSystem(5.0)
    
    ticker.subscribe(portfolio1, "price_update")
    ticker.subscribe(portfolio2, "price_update")
    ticker.subscribe(alert_system, "price_increase")
    ticker.subscribe(alert_system, "price_decrease")
    
    ticker.price = 150.00
    ticker.price = 157.50
    ticker.price = 145.25
    
    ticker.unsubscribe(portfolio1, "price_update")
    ticker.price = 152.00
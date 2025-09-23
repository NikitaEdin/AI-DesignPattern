from abc import ABC, abstractmethod
from typing import Dict, Set, Any, Callable, Optional
from weakref import WeakSet
import threading

class Subscriber(ABC):
    @abstractmethod
    def notify(self, event_type: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._subscribers: Dict[str, WeakSet] = {}
        self._lock = threading.RLock()
        
    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = WeakSet()
            self._subscribers[event_type].add(subscriber)
    
    def unsubscribe(self, event_type: str, subscriber: Subscriber) -> None:
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type].discard(subscriber)
    
    def publish(self, event_type: str, data: Any = None) -> None:
        with self._lock:
            if event_type in self._subscribers:
                subscribers_copy = list(self._subscribers[event_type])
        
        for subscriber in subscribers_copy:
            try:
                subscriber.notify(event_type, data)
            except Exception as e:
                self._handle_notification_error(subscriber, event_type, e)
    
    def _handle_notification_error(self, subscriber: Subscriber, event_type: str, error: Exception) -> None:
        print(f"Error notifying {subscriber.__class__.__name__} for {event_type}: {error}")

class SmartPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self._filters: Dict[str, Callable[[Any], bool]] = {}
    
    def add_filter(self, event_type: str, filter_func: Callable[[Any], bool]) -> None:
        self._filters[event_type] = filter_func
    
    def publish(self, event_type: str, data: Any = None) -> None:
        if event_type in self._filters and not self._filters[event_type](data):
            return
        super().publish(event_type, data)

class StockPriceMonitor(SmartPublisher):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol
        self._price = 0.0
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, new_price: float) -> None:
        old_price = self._price
        self._price = new_price
        
        change_data = {
            'symbol': self.symbol,
            'old_price': old_price,
            'new_price': new_price,
            'change': new_price - old_price
        }
        
        self.publish('price_changed', change_data)
        
        if new_price > old_price:
            self.publish('price_increased', change_data)
        elif new_price < old_price:
            self.publish('price_decreased', change_data)

class TradingBot(Subscriber):
    def __init__(self, name: str):
        self.name = name
    
    def notify(self, event_type: str, data: Any) -> None:
        if event_type == 'price_increased' and data['change'] > 5:
            print(f"{self.name}: SELL signal for {data['symbol']} at ${data['new_price']:.2f}")
        elif event_type == 'price_decreased' and data['change'] < -3:
            print(f"{self.name}: BUY signal for {data['symbol']} at ${data['new_price']:.2f}")

class PriceDisplay(Subscriber):
    def notify(self, event_type: str, data: Any) -> None:
        if event_type == 'price_changed':
            direction = "↑" if data['change'] > 0 else "↓" if data['change'] < 0 else "→"
            print(f"Display: {data['symbol']} {direction} ${data['new_price']:.2f} ({data['change']:+.2f})")

if __name__ == "__main__":
    stock = StockPriceMonitor("AAPL")
    
    stock.add_filter('price_increased', lambda data: data['change'] > 1.0)
    
    bot1 = TradingBot("AlgoBot-1")
    bot2 = TradingBot("AlgoBot-2")
    display = PriceDisplay()
    
    stock.subscribe('price_changed', display)
    stock.subscribe('price_increased', bot1)
    stock.subscribe('price_decreased', bot1)
    stock.subscribe('price_increased', bot2)
    stock.subscribe('price_decreased', bot2)
    
    print("Stock price simulation:")
    stock.price = 150.0
    stock.price = 155.5
    stock.price = 148.2
    stock.price = 149.0
    
    stock.unsubscribe('price_increased', bot2)
    print("\nAfter unsubscribing bot2 from increases:")
    stock.price = 154.0
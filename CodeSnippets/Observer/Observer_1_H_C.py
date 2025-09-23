from abc import ABC, abstractmethod
from typing import List, Any, Callable, Optional
from functools import wraps
import weakref

class Subscriber(ABC):
    @abstractmethod
    def notify(self, event_type: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._subscribers = weakref.WeakSet()
        self._event_filters = {}
        
    def add_subscriber(self, subscriber: Subscriber, event_filter: Optional[Callable[[str], bool]] = None):
        self._subscribers.add(subscriber)
        if event_filter:
            self._event_filters[subscriber] = event_filter
            
    def remove_subscriber(self, subscriber: Subscriber):
        self._subscribers.discard(subscriber)
        self._event_filters.pop(subscriber, None)
        
    def broadcast(self, event_type: str, data: Any = None):
        for subscriber in list(self._subscribers):
            try:
                filter_func = self._event_filters.get(subscriber)
                if not filter_func or filter_func(event_type):
                    subscriber.notify(event_type, data)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")

def event_publisher(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, '_publisher'):
            self._publisher.broadcast(func.__name__, {'args': args, 'kwargs': kwargs, 'result': result})
        return result
    return wrapper

class StockPrice(Publisher):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self._symbol = symbol
        self._price = price
        self._publisher = self
        
    @property
    def price(self):
        return self._price
        
    @event_publisher
    def update_price(self, new_price: float):
        old_price = self._price
        self._price = new_price
        return {'symbol': self._symbol, 'old_price': old_price, 'new_price': new_price}
        
    @event_publisher
    def split_stock(self, ratio: float):
        self._price /= ratio
        return {'symbol': self._symbol, 'ratio': ratio, 'new_price': self._price}

class Portfolio(Subscriber):
    def __init__(self, name: str):
        self.name = name
        self.holdings = {}
        
    def add_holding(self, symbol: str, shares: int):
        self.holdings[symbol] = shares
        
    def notify(self, event_type: str, data: Any):
        event_data = data.get('result', {})
        symbol = event_data.get('symbol')
        
        if symbol in self.holdings:
            if event_type == 'update_price':
                print(f"{self.name}: {symbol} price changed from ${event_data['old_price']:.2f} to ${event_data['new_price']:.2f}")
            elif event_type == 'split_stock':
                self.holdings[symbol] *= event_data['ratio']
                print(f"{self.name}: {symbol} split {event_data['ratio']}:1, now own {self.holdings[symbol]} shares")

class AlertSystem(Subscriber):
    def __init__(self, threshold: float):
        self.threshold = threshold
        
    def notify(self, event_type: str, data: Any):
        if event_type == 'update_price':
            event_data = data.get('result', {})
            price_change = abs(event_data['new_price'] - event_data['old_price'])
            if price_change > self.threshold:
                print(f"ALERT: {event_data['symbol']} price changed by ${price_change:.2f}")

if __name__ == "__main__":
    stock = StockPrice("AAPL", 150.00)
    
    portfolio1 = Portfolio("Tech Portfolio")
    portfolio1.add_holding("AAPL", 100)
    
    portfolio2 = Portfolio("Growth Portfolio")
    portfolio2.add_holding("AAPL", 50)
    portfolio2.add_holding("GOOGL", 25)
    
    alert_system = AlertSystem(5.0)
    
    stock.add_subscriber(portfolio1)
    stock.add_subscriber(portfolio2, lambda event: event in ['update_price', 'split_stock'])
    stock.add_subscriber(alert_system, lambda event: event == 'update_price')
    
    stock.update_price(155.50)
    stock.update_price(148.25)
    stock.split_stock(2.0)
    
    stock.remove_subscriber(portfolio1)
    stock.update_price(80.00)
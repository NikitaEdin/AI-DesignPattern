from abc import ABC, abstractmethod
from typing import Set, Any, Dict, Callable
from functools import wraps
import weakref

class Subscriber(ABC):
    @abstractmethod
    def notify(self, source: Any, event_type: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._subscribers: Dict[str, Set[weakref.ReferenceType]] = {}
        self._event_filters: Dict[str, Callable] = {}
    
    def subscribe(self, subscriber: Subscriber, event_type: str = "*") -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = set()
        self._subscribers[event_type].add(weakref.ref(subscriber))
    
    def unsubscribe(self, subscriber: Subscriber, event_type: str = "*") -> None:
        if event_type in self._subscribers:
            to_remove = {ref for ref in self._subscribers[event_type] 
                        if ref() is subscriber}
            self._subscribers[event_type] -= to_remove
    
    def add_filter(self, event_type: str, filter_func: Callable) -> None:
        self._event_filters[event_type] = filter_func
    
    def emit(self, event_type: str, data: Any = None) -> None:
        if event_type in self._event_filters:
            if not self._event_filters[event_type](data):
                return
        
        all_subscribers = set()
        if "*" in self._subscribers:
            all_subscribers.update(self._subscribers["*"])
        if event_type in self._subscribers:
            all_subscribers.update(self._subscribers[event_type])
        
        dead_refs = set()
        for ref in all_subscribers:
            subscriber = ref()
            if subscriber is None:
                dead_refs.add(ref)
            else:
                try:
                    subscriber.notify(self, event_type, data)
                except Exception:
                    pass
        
        self._cleanup_dead_references(dead_refs)
    
    def _cleanup_dead_references(self, dead_refs: Set[weakref.ReferenceType]) -> None:
        for event_type, refs in self._subscribers.items():
            refs -= dead_refs

def event_publisher(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        event_name = f"{method.__name__}_completed"
        if hasattr(self, 'emit'):
            self.emit(event_name, {'args': args, 'kwargs': kwargs, 'result': result})
        return result
    return wrapper

class StockMarket(Publisher):
    def __init__(self):
        super().__init__()
        self._prices: Dict[str, float] = {}
    
    @event_publisher
    def update_price(self, symbol: str, price: float) -> None:
        old_price = self._prices.get(symbol, 0)
        self._prices[symbol] = price
        
        change_type = "price_increase" if price > old_price else "price_decrease"
        self.emit("price_change", {"symbol": symbol, "price": price, "old_price": old_price})
        self.emit(change_type, {"symbol": symbol, "price": price, "change": price - old_price})

class Trader(Subscriber):
    def __init__(self, name: str):
        self.name = name
        self.portfolio = []
    
    def notify(self, source: Any, event_type: str, data: Any) -> None:
        if event_type == "price_increase" and data["change"] > 5:
            self.portfolio.append(f"BUY {data['symbol']} at ${data['price']}")
        elif event_type == "price_decrease" and data["change"] < -3:
            self.portfolio.append(f"SELL {data['symbol']} at ${data['price']}")

class NewsAgency(Subscriber):
    def __init__(self):
        self.headlines = []
    
    def notify(self, source: Any, event_type: str, data: Any) -> None:
        if event_type == "price_change":
            symbol, price = data["symbol"], data["price"]
            self.headlines.append(f"BREAKING: {symbol} now trading at ${price}")

if __name__ == "__main__":
    market = StockMarket()
    
    trader1 = Trader("Alice")
    trader2 = Trader("Bob")
    news = NewsAgency()
    
    market.subscribe(trader1, "price_increase")
    market.subscribe(trader2, "price_decrease")
    market.subscribe(news, "price_change")
    
    market.add_filter("price_increase", lambda data: data["price"] > 10)
    
    market.update_price("AAPL", 150.0)
    market.update_price("AAPL", 157.0)
    market.update_price("AAPL", 152.0)
    
    print(f"Trader1 actions: {trader1.portfolio}")
    print(f"Trader2 actions: {trader2.portfolio}")
    print(f"News headlines: {news.headlines}")
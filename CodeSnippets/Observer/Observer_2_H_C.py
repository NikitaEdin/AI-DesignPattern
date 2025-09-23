from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from weakref import WeakSet
import threading

class Subscriber(ABC):
    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        pass

class Publisher:
    def __init__(self):
        self._subscribers: Dict[str, WeakSet] = {}
        self._lock = threading.RLock()
    
    def subscribe(self, event: str, subscriber: Subscriber, condition: Optional[Callable] = None):
        with self._lock:
            if event not in self._subscribers:
                self._subscribers[event] = WeakSet()
            if condition:
                subscriber._condition = condition
            self._subscribers[event].add(subscriber)
    
    def unsubscribe(self, event: str, subscriber: Subscriber):
        with self._lock:
            if event in self._subscribers:
                self._subscribers[event].discard(subscriber)
    
    def notify(self, event: str, data: Any = None):
        with self._lock:
            if event in self._subscribers:
                for subscriber in list(self._subscribers[event]):
                    try:
                        condition = getattr(subscriber, '_condition', None)
                        if condition is None or condition(data):
                            subscriber.update(event, data)
                    except Exception as e:
                        print(f"Error notifying subscriber: {e}")

class StockMarket(Publisher):
    def __init__(self):
        super().__init__()
        self._prices: Dict[str, float] = {}
    
    def set_price(self, symbol: str, price: float):
        old_price = self._prices.get(symbol, 0)
        self._prices[symbol] = price
        
        self.notify("price_changed", {"symbol": symbol, "price": price, "old_price": old_price})
        
        if price > old_price:
            self.notify("price_increased", {"symbol": symbol, "price": price})
        elif price < old_price:
            self.notify("price_decreased", {"symbol": symbol, "price": price})

class Trader(Subscriber):
    def __init__(self, name: str):
        self.name = name
        self.portfolio: Dict[str, int] = {}
    
    def update(self, event: str, data: Any):
        symbol = data["symbol"]
        price = data["price"]
        print(f"{self.name} received {event}: {symbol} at ${price:.2f}")

class Portfolio(Subscriber):
    def __init__(self, name: str):
        self.name = name
        self.holdings: Dict[str, Dict] = {}
    
    def add_holding(self, symbol: str, shares: int, avg_price: float):
        self.holdings[symbol] = {"shares": shares, "avg_price": avg_price}
    
    def update(self, event: str, data: Any):
        if event == "price_changed":
            symbol = data["symbol"]
            if symbol in self.holdings:
                current_value = self.holdings[symbol]["shares"] * data["price"]
                print(f"Portfolio {self.name}: {symbol} value is now ${current_value:.2f}")

class AlertSystem(Subscriber):
    def __init__(self):
        self.alerts: List[str] = []
    
    def update(self, event: str, data: Any):
        if event in ["price_increased", "price_decreased"]:
            alert = f"ALERT: {data['symbol']} {event.split('_')[1]} to ${data['price']:.2f}"
            self.alerts.append(alert)
            print(alert)

if __name__ == "__main__":
    market = StockMarket()
    
    trader1 = Trader("Alice")
    trader2 = Trader("Bob")
    portfolio = Portfolio("TechFund")
    alerts = AlertSystem()
    
    market.subscribe("price_changed", trader1)
    market.subscribe("price_increased", trader2, lambda data: data["price"] > 100)
    market.subscribe("price_changed", portfolio)
    market.subscribe("price_increased", alerts)
    market.subscribe("price_decreased", alerts)
    
    portfolio.add_holding("AAPL", 100, 150.0)
    portfolio.add_holding("GOOGL", 50, 2500.0)
    
    print("=== Market Updates ===")
    market.set_price("AAPL", 155.50)
    market.set_price("GOOGL", 2600.75)
    market.set_price("TSLA", 120.25)
    market.set_price("AAPL", 152.00)
    
    market.unsubscribe("price_changed", trader1)
    print("\n=== After Alice unsubscribed ===")
    market.set_price("AAPL", 160.00)
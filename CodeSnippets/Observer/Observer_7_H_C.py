import weakref
from typing import Any, Dict, List, Set
from abc import ABC, abstractmethod

class Publisher:
    def __init__(self):
        self._listeners: Dict[str, Set[weakref.ReferenceType]] = {}
    
    def subscribe(self, event_type: str, listener_obj: Any):
        if event_type not in self._listeners:
            self._listeners[event_type] = set()
        
        def cleanup_callback(ref):
            self._listeners[event_type].discard(ref)
        
        weak_ref = weakref.ref(listener_obj, cleanup_callback)
        self._listeners[event_type].add(weak_ref)
    
    def unsubscribe(self, event_type: str, listener_obj: Any):
        if event_type in self._listeners:
            to_remove = [ref for ref in self._listeners[event_type] 
                        if ref() is listener_obj]
            for ref in to_remove:
                self._listeners[event_type].discard(ref)
    
    def notify(self, event_type: str, data: Any):
        if event_type not in self._listeners:
            return
        
        dead_refs = []
        for weak_ref in self._listeners[event_type].copy():
            listener = weak_ref()
            if listener is None:
                dead_refs.append(weak_ref)
            else:
                try:
                    listener.update(event_type, data)
                except Exception as e:
                    print(f"Error notifying listener: {e}")
        
        for dead_ref in dead_refs:
            self._listeners[event_type].discard(dead_ref)

class Listener(ABC):
    @abstractmethod
    def update(self, event_type: str, data: Any):
        pass

class StockPrice(Publisher):
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
        
        if value > old_price * 1.05:
            self.notify("price_surge", {"symbol": self.symbol, "price": value, "change": value - old_price})
        elif value < old_price * 0.95:
            self.notify("price_drop", {"symbol": self.symbol, "price": value, "change": value - old_price})
        else:
            self.notify("price_change", {"symbol": self.symbol, "price": value, "change": value - old_price})

class Display(Listener):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, event_type: str, data: Any):
        print(f"[{self.name}] {event_type}: {data['symbol']} = ${data['price']:.2f}")

class AlertSystem(Listener):
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def update(self, event_type: str, data: Any):
        if event_type in ["price_surge", "price_drop"] and abs(data['change']) > self.threshold:
            print(f"ALERT: {data['symbol']} major movement: {data['change']:+.2f}")

if __name__ == "__main__":
    stock = StockPrice("TECH")
    
    display1 = Display("Dashboard")
    display2 = Display("Mobile")
    alert = AlertSystem(5.0)
    
    stock.subscribe("price_change", display1)
    stock.subscribe("price_surge", display1)
    stock.subscribe("price_drop", display1)
    stock.subscribe("price_change", display2)
    stock.subscribe("price_surge", alert)
    stock.subscribe("price_drop", alert)
    
    stock.price = 100.0
    stock.price = 107.0
    stock.price = 105.0
    stock.price = 95.0
    
    del display2
    stock.price = 110.0
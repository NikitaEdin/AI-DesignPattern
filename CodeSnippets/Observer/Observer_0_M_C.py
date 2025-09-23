from abc import ABC, abstractmethod

class Listener(ABC):
    @abstractmethod
    def notify(self, data):
        pass

class Subject:
    def __init__(self):
        self._listeners = []
    
    def subscribe(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)
    
    def unsubscribe(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_all(self, data):
        for listener in self._listeners[:]:
            try:
                listener.notify(data)
            except Exception as e:
                print(f"Error notifying listener: {e}")

class StockPrice(Subject):
    def __init__(self, symbol):
        super().__init__()
        self._symbol = symbol
        self._price = 0
    
    def set_price(self, price):
        self._price = price
        self._notify_all({'symbol': self._symbol, 'price': price})

class EmailNotifier(Listener):
    def __init__(self, email):
        self.email = email
    
    def notify(self, data):
        print(f"Email to {self.email}: {data['symbol']} is now ${data['price']}")

class SMSNotifier(Listener):
    def __init__(self, phone):
        self.phone = phone
    
    def notify(self, data):
        print(f"SMS to {self.phone}: {data['symbol']} price alert: ${data['price']}")

if __name__ == "__main__":
    stock = StockPrice("AAPL")
    
    email_user = EmailNotifier("user@email.com")
    sms_user = SMSNotifier("555-1234")
    
    stock.subscribe(email_user)
    stock.subscribe(sms_user)
    
    stock.set_price(150.25)
    stock.set_price(152.80)
    
    stock.unsubscribe(email_user)
    stock.set_price(148.90)
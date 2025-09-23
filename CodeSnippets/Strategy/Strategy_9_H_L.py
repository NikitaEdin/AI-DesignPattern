class OrderStrategy(object):
    def execute(self, order):
        raise NotImplementedError("execute method must be implemented by subclass")
        
class BuyOrderStrategy(OrderStrategy):
    def execute(self, order):
        print("Executing buy order...")
        
class SellOrderStrategy(OrderStrategy):
    def execute(self, order):
        print("Executing sell order...")
        
class Order:
    def __init__(self, stock, quantity, price, strategy):
        self.stock = stock
        self.quantity = quantity
        self.price = price
        self.strategy = strategy
        
    def execute(self):
        self.strategy.execute(self)
        
# Example usage
order = Order("AAPL", 100, 100.0, BuyOrderStrategy())
order.execute() # Executing buy order...
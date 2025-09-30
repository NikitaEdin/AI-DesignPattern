class PaymentGateway:
    def __init__(self):
        self.balance = 1000
    
    def verify_balance(self, amount):
        return self.balance >= amount
    
    def deduct(self, amount):
        self.balance -= amount

class InventoryManager:
    def __init__(self):
        self.items = {"book": 10, "pen": 20}
    
    def check_stock(self, item):
        return self.items.get(item, 0) > 0
    
    def reserve_item(self, item):
        if self.check_stock(item):
            self.items[item] -= 1
            return True
        return False

class ShippingService:
    def __init__(self):
        self.order_id = 1000
    
    def schedule_delivery(self, address):
        self.order_id += 1
        return self.order_id

class OrderProcessor:
    def __init__(self):
        self.payment = PaymentGateway()
        self.inventory = InventoryManager()
        self.shipping = ShippingService()
    
    def place_order(self, item, price, address):
        try:
            if not self.inventory.check_stock(item):
                return False
            
            if not self.payment.verify_balance(price):
                return False
            
            self.inventory.reserve_item(item)
            self.payment.deduct(price)
            order_id = self.shipping.schedule_delivery(address)
            return order_id
        except Exception:
            return False

if __name__ == "__main__":
    processor = OrderProcessor()
    result = processor.place_order("book", 50, "123 Main St")
    print(result)
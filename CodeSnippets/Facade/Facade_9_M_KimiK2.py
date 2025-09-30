class InventoryService:
    def check_stock(self, product_id):
        stock = {"P100": 5, "P200": 0}
        return stock.get(product_id, 0)

class PaymentService:
    def process(self, payment_info):
        return payment_info['amount'] > 0 and len(payment_info['card']) == 16

class ShippingService:
    def dispatch(self, address):
        return bool(address and len(address) > 5)

class OrderManager:
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
    
    def place_order(self, product_id, payment_info, address):
        if self.inventory.check_stock(product_id) == 0:
            return False, "Out of stock"
        if not self.payment.process(payment_info):
            return False, "Payment failed"
        if not self.shipping.dispatch(address):
            pinfo = payment_info.copy()
            pinfo['card'] = pinfo['card'][-4:]
            return False, "Invalid address"
        return True, "Order placed successfully"

if __name__ == "__main__":
    manager = OrderManager()
    ok, msg = manager.place_order("P100", {"amount": 59.99, "card": "1234567890123456"}, "123 Main St")
    print(ok, msg)
    ok, msg = manager.place_order("P200", {"amount": 59.99, "card": "1234567890123456"}, "123 Main St")
    print(ok, msg)
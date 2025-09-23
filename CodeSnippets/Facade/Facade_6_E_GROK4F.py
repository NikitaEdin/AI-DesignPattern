class Inventory:
    def check_stock(self, item):
        return True

    def update_stock(self, item):
        pass

class Payment:
    def process_payment(self, amount):
        return True

class Shipping:
    def handle_shipment(self, item):
        pass

class OrderManager:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()

    def process_order(self, item, amount):
        if self.inventory.check_stock(item):
            if self.payment.process_payment(amount):
                self.inventory.update_stock(item)
                self.shipping.handle_shipment(item)
                return "Order processed successfully"
        return "Order processing failed"

if __name__ == "__main__":
    manager = OrderManager()
    result = manager.process_order("laptop", 999)
    print(result)
class PaymentProcessor:
    def process(self, amount):
        print(f"Processing payment of {amount}")

class InventoryManager:
    def check_stock(self, item):
        print(f"Checking stock for {item}")
    def reserve(self, item):
        print(f"Reserving {item}")

class ShippingService:
    def ship(self, item, address):
        print(f"Shipping {item} to {address}")

class OrderProcessor:
    def __init__(self):
        self.payment = PaymentProcessor()
        self.inventory = InventoryManager()
        self.shipping = ShippingService()

    def process_order(self, item, amount, address):
        self.inventory.check_stock(item)
        self.inventory.reserve(item)
        self.payment.process(amount)
        self.shipping.ship(item, address)

if __name__ == "__main__":
    processor = OrderProcessor()
    processor.process_order("laptop", 1000, "123 Main St")
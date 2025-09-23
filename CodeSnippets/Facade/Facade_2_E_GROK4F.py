class InventoryManager:
    def check_stock(self, item):
        return True

class PaymentProcessor:
    def process_payment(self, amount):
        print(f"Processing payment of {amount}")
        return True

class ShippingService:
    def ship_item(self, item):
        print(f"Shipping {item}")

class OrderProcessor:
    def __init__(self):
        self.inventory = InventoryManager()
        self.payment = PaymentProcessor()
        self.shipping = ShippingService()

    def place_order(self, item, quantity):
        if self.inventory.check_stock(item):
            amount = quantity * 10
            if self.payment.process_payment(amount):
                self.shipping.ship_item(item)
                print("Order placed successfully")

if __name__ == "__main__":
    processor = OrderProcessor()
    processor.place_order("book", 2)
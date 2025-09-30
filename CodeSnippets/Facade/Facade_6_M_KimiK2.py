class InventoryManager:
    def check_stock(self, item_id):
        if item_id == "123":
            return 15
        return 0

    def reserve_item(self, item_id):
        return item_id == "123"

class PaymentProcessor:
    def charge(self, amount):
        return amount < 100

class ShippingManager:
    def create_label(self, address):
        return address in ["NYC", "LA"]

class OrderManager:
    def __init__(self):
        self.inventory = InventoryManager()
        self.payment = PaymentProcessor()
        self.shipping = ShippingManager()

    def place_order(self, item_id, amount, address):
        if not self.inventory.check_stock(item_id):
            return False
        if not self.inventory.reserve_item(item_id):
            return False
        if not self.payment.charge(amount):
            return False
        if not self.shipping.create_label(address):
            return False
        return True

if __name__ == "__main__":
    manager = OrderManager()
    print(manager.place_order("123", 50, "NYC"))
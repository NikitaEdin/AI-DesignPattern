class AuthService:
    def validate_user(self, username, password):
        return username == "admin" and password == "secret"

class PaymentGateway:
    def process_payment(self, amount):
        return amount > 0

class InventoryManager:
    def check_stock(self, item_id, quantity):
        return item_id.startswith("SKU") and quantity <= 100

class ShippingProvider:
    def schedule_delivery(self, address):
        return "processed" if address else None

class OrderCoordinator:
    def __init__(self):
        self.auth = AuthService()
        self.payment = PaymentGateway()
        self.inventory = InventoryManager()
        self.shipping = ShippingProvider()
    
    def place_order(self, username, password, item_id, quantity, amount, address):
        if not self.auth.validate_user(username, password):
            return {"status": "failed", "reason": "authentication"}
        if not self.inventory.check_stock(item_id, quantity):
            return {"status": "failed", "reason": "stock"}
        if not self.payment.process_payment(amount):
            return {"status": "failed", "reason": "payment"}
        tracking = self.shipping.schedule_delivery(address)
        return {"status": "success", "tracking": tracking}

if __name__ == "__main__":
    coordinator = OrderCoordinator()
    result = coordinator.place_order("admin", "secret", "SKU123", 10, 99.99, "123 Main St")
    print(result)
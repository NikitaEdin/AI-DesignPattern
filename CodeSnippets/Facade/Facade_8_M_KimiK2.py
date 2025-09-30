import time

class InventorySystem:
    def check_stock(self, product: str, quantity: int) -> bool:
        print(f"Verifying stock for {product}...")
        time.sleep(0.1)
        return product == "laptop" and quantity <= 5

class PaymentGateway:
    def process_payment(self, amount: float) -> bool:
        print(f"Processing payment of ${amount}...")
        time.sleep(0.1)
        return amount < 2000

class ShippingService:
    def schedule_delivery(self, address: str) -> str:
        print(f"Scheduling delivery to {address}...")
        time.sleep(0.1)
        return "DEL123"

class OrderProcessor:
    def __init__(self):
        self.inventory = InventorySystem()
        self.payment = PaymentGateway()
        self.shipping = ShippingService()

    def order(self, product: str, quantity: int, amount: float, address: str) -> dict:
        if not self.inventory.check_stock(product, quantity):
            return {"status": "failed", "reason": "Out of stock"}
        if not self.payment.process_payment(amount):
            raise RuntimeError("Payment declined")
        tracking = self.shipping.schedule_delivery(address)
        return {"status": "confirmed", "tracking": tracking}

if __name__ == "__main__":
    processor = OrderProcessor()
    try:
        result = processor.order("laptop", 1, 999.99, "42 Wallaby Way")
        print("Order result:", result)
    except RuntimeError as e:
        print("Order error:", e)
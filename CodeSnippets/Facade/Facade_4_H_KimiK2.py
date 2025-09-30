import threading
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class OrderDetails:
    items: Dict[str, int]
    payment_method: str
    shipping_address: str
    customer_email: str

class InventoryManager:
    def __init__(self):
        self._stock = {"laptop": 10, "mouse": 50, "keyboard": 30}
        self._lock = threading.Lock()
    
    def check_availability(self, items: Dict[str, int]) -> bool:
        with self._lock:
            return all(self._stock.get(item, 0) >= qty for item, qty in items.items())
    
    def reserve_items(self, items: Dict[str, int]) -> bool:
        with self._lock:
            if not self.check_availability(items):
                return False
            for item, qty in items.items():
                self._stock[item] -= qty
            return True
    
    def release_items(self, items: Dict[str, int]):
        with self._lock:
            for item, qty in items.items():
                self._stock[item] += qty

class PaymentProcessor:
    def __init__(self):
        self._processing_lock = threading.Lock()
    
    def process_payment(self, amount: float, method: str) -> bool:
        with self._processing_lock:
            time.sleep(0.1)
            return method in ["credit_card", "paypal", "crypto"]

class ShippingCoordinator:
    def __init__(self):
        self._tracking_numbers = {}
        self._counter = 0
    
    def schedule_delivery(self, address: str, items: Dict[str, int]) -> str:
        self._counter += 1
        tracking = f"TRK{self._counter:06d}"
        self._tracking_numbers[tracking] = {"address": address, "items": items, "status": "processing"}
        return tracking
    
    def get_status(self, tracking: str) -> Optional[str]:
        return self._tracking_numbers.get(tracking, {}).get("status")

class NotificationService:
    def send_confirmation(self, email: str, tracking: str, items: Dict[str, int]):
        print(f"📧 Email sent to {email}: Order confirmed! Tracking: {tracking}")
    
    def send_failure(self, email: str, reason: str):
        print(f"📧 Email sent to {email}: Order failed - {reason}")

class OrderCoordinator:
    def __init__(self):
        self.inventory = InventoryManager()
        self.payment = PaymentProcessor()
        self.shipping = ShippingCoordinator()
        self.notifications = NotificationService()
    
    def place_order(self, details: OrderDetails) -> Dict[str, Any]:
        try:
            if not self.inventory.check_availability(details.items):
                self.notifications.send_failure(details.customer_email, "Items out of stock")
                return {"success": False, "error": "Out of stock"}
            
            total = sum(100 * qty for item, qty in details.items.items())
            
            if not self.payment.process_payment(total, details.payment_method):
                self.notifications.send_failure(details.customer_email, "Payment failed")
                return {"success": False, "error": "Payment declined"}
            
            if not self.inventory.reserve_items(details.items):
                self.notifications.send_failure(details.customer_email, "Stock changed during checkout")
                return {"success": False, "error": "Stock conflict"}
            
            tracking = self.shipping.schedule_delivery(details.shipping_address, details.items)
            self.notifications.send_confirmation(details.customer_email, tracking, details.items)
            
            return {
                "success": True,
                "tracking": tracking,
                "total": total,
                "items": details.items
            }
            
        except Exception as e:
            self.inventory.release_items(details.items)
            self.notifications.send_failure(details.customer_email, str(e))
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    coordinator = OrderCoordinator()
    
    order = OrderDetails(
        items={"laptop": 1, "mouse": 2},
        payment_method="credit_card",
        shipping_address="123 Tech Street, Silicon Valley",
        customer_email="customer@example.com"
    )
    
    result = coordinator.place_order(order)
    print(f"Order result: {result}")
    
    if result["success"]:
        status = coordinator.shipping.get_status(result["tracking"])
        print(f"Shipping status: {status}")
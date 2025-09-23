import uuid
import random

class AuthService:
    def authenticate(self, user_id: str) -> bool:
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user identifier")
        return not user_id.startswith("blocked_")

class InventoryService:
    def __init__(self):
        self._stock = {"widget": 10, "gadget": 5}

    def reserve(self, item_id: str, quantity: int) -> str:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        available = self._stock.get(item_id, 0)
        if available < quantity:
            raise RuntimeError("Insufficient stock")
        self._stock[item_id] = available - quantity
        return f"resv-{uuid.uuid4().hex[:8]}"

    def release(self, item_id: str, quantity: int) -> None:
        if quantity <= 0:
            return
        self._stock[item_id] = self._stock.get(item_id, 0) + quantity

class PaymentService:
    def charge(self, card_info: dict, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Charge amount must be positive")
        if not card_info.get("number") or len(str(card_info.get("number"))) < 12:
            raise RuntimeError("Invalid card information")
        if random.random() < 0.1:
            raise RuntimeError("Payment gateway error")
        return f"txn-{uuid.uuid4().hex[:8]}"

class OrderCoordinator:
    def __init__(self, auth: AuthService, inventory: InventoryService, payment: PaymentService):
        self._auth = auth
        self._inventory = inventory
        self._payment = payment

    def place_order(self, user_id: str, item_id: str, quantity: int, card_info: dict, dry_run: bool = False) -> dict:
        if not self._auth.authenticate(user_id):
            raise PermissionError("User not authorized")
        if dry_run:
            available = self._inventory._stock.get(item_id, 0)
            return {"status": "dry_run", "available": available, "can_fulfill": available >= quantity}
        reservation_id = None
        try:
            reservation_id = self._inventory.reserve(item_id, quantity)
            price = self._calculate_price(item_id, quantity)
            transaction_id = self._payment.charge(card_info, price)
            order_id = f"order-{uuid.uuid4().hex[:8]}"
            return {"status": "confirmed", "order_id": order_id, "reservation": reservation_id, "transaction": transaction_id, "amount": price}
        except Exception as e:
            if reservation_id:
                try:
                    self._inventory.release(item_id, quantity)
                except Exception:
                    pass
            raise

    def _calculate_price(self, item_id: str, quantity: int) -> float:
        base = {"widget": 19.99, "gadget": 29.99}.get(item_id, 9.99)
        return round(base * quantity, 2)

if __name__ == "__main__":
    auth = AuthService()
    inventory = InventoryService()
    payment = PaymentService()
    coordinator = OrderCoordinator(auth, inventory, payment)

    try:
        result = coordinator.place_order("user123", "widget", 2, {"number": "424242424242"}, dry_run=True)
        print("Dry run:", result)
        result = coordinator.place_order("user123", "widget", 2, {"number": "424242424242"})
        print("Order result:", result)
    except Exception as err:
        print("Error:", type(err).__name__, str(err))
import random
import time

class AuthenticationError(Exception):
    pass

class PaymentError(Exception):
    pass

class InventoryError(Exception):
    pass

class AuthService:
    def __init__(self, valid_users):
        self.valid_users = set(valid_users)

    def validate_user(self, username):
        if username not in self.valid_users:
            raise AuthenticationError(f"Unknown user: {username}")
        return True

class InventoryService:
    def __init__(self):
        self.stock = {}

    def add_stock(self, item, qty):
        self.stock[item] = self.stock.get(item, 0) + qty

    def reserve_item(self, item, qty):
        available = self.stock.get(item, 0)
        if available < qty:
            raise InventoryError(f"Insufficient stock for {item}")
        self.stock[item] = available - qty
        return True

    def release_item(self, item, qty):
        self.stock[item] = self.stock.get(item, 0) + qty
        return True

class PaymentService:
    def __init__(self, fail_rate=0.2):
        self.fail_rate = fail_rate

    def charge(self, user, amount):
        if amount <= 0:
            raise PaymentError("Invalid amount")
        if random.random() < self.fail_rate:
            raise PaymentError("Transient payment gateway error")
        return {"status": "charged", "amount": amount, "user": user}

class NotificationService:
    def send_receipt(self, user, order_id, details):
        return f"Receipt for {user}: order {order_id} processed with {details}"

class OrderCoordinator:
    def __init__(self, auth, inventory, payment, notifier, max_retries=3, retry_delay=0.5):
        self.auth = auth
        self.inventory = inventory
        self.payment = payment
        self.notifier = notifier
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def process_order(self, order_id, user, items, amount):
        self.auth.validate_user(user)
        reserved = []
        try:
            for item, qty in items.items():
                self.inventory.reserve_item(item, qty)
                reserved.append((item, qty))
            attempt = 0
            while True:
                try:
                    result = self.payment.charge(user, amount)
                    break
                except PaymentError as e:
                    attempt += 1
                    if attempt >= self.max_retries:
                        raise
                    time.sleep(self.retry_delay)
            receipt = self.notifier.send_receipt(user, order_id, result)
            return {"order_id": order_id, "status": "completed", "receipt": receipt}
        except Exception:
            for item, qty in reserved:
                try:
                    self.inventory.release_item(item, qty)
                except Exception:
                    pass
            raise

if __name__ == "__main__":
    random.seed(1)
    auth = AuthService(valid_users=["alice", "bob"])
    inv = InventoryService()
    inv.add_stock("widget", 5)
    inv.add_stock("gadget", 2)
    pay = PaymentService(fail_rate=0.5)
    note = NotificationService()
    coordinator = OrderCoordinator(auth, inv, pay, note, max_retries=4, retry_delay=0.1)

    try:
        result = coordinator.process_order("ORD-1001", "alice", {"widget": 2, "gadget": 1}, 120.0)
        print(result)
    except Exception as e:
        print("Order failed:", e)

    try:
        result = coordinator.process_order("ORD-1002", "eve", {"widget": 1}, 40.0)
        print(result)
    except Exception as e:
        print("Order failed:", e)
class AuthenticationError(Exception):
    pass

class InventoryError(Exception):
    pass

class PaymentError(Exception):
    pass

class AuthService:
    def __init__(self, users):
        self.users = users

    def authenticate(self, user_id):
        user = self.users.get(user_id)
        if not user or not user.get("active"):
            raise AuthenticationError("User not authenticated or inactive")
        return user

class InventoryService:
    def __init__(self, stock):
        self.stock = stock

    def reserve_item(self, item_id, quantity):
        available = self.stock.get(item_id, 0)
        if quantity <= 0 or quantity > available:
            raise InventoryError("Insufficient stock for item")
        self.stock[item_id] = available - quantity
        return True

    def release_item(self, item_id, quantity):
        self.stock[item_id] = self.stock.get(item_id, 0) + quantity
        return True

class PaymentService:
    def charge(self, card_info, amount):
        if amount <= 0:
            raise PaymentError("Invalid charge amount")
        if card_info.get("number", "").endswith("0000"):
            raise PaymentError("Card declined")
        return {"status": "charged", "amount": amount, "transaction_id": "tx123"}

class NotificationService:
    def send_email(self, email, subject, body):
        if "@" not in email:
            raise ValueError("Invalid email address")
        print(f"Email to {email}: {subject}\n{body}")
        return True

class OrderProcessor:
    def __init__(self, auth, inventory, payment, notifier, max_payment_attempts=2):
        self.auth = auth
        self.inventory = inventory
        self.payment = payment
        self.notifier = notifier
        self.max_attempts = max_payment_attempts

    def place_order(self, user_id, item_id, quantity, card_info):
        user = self.auth.authenticate(user_id)
        try:
            self.inventory.reserve_item(item_id, quantity)
        except InventoryError as e:
            raise
        attempt = 0
        while attempt < self.max_attempts:
            attempt += 1
            try:
                receipt = self.payment.charge(card_info, amount=quantity * 10)
                self.notifier.send_email(user["email"], "Order Confirmed", f"Item {item_id} x{quantity}\nReceipt: {receipt['transaction_id']}")
                return {"status": "success", "transaction": receipt}
            except PaymentError:
                if attempt >= self.max_attempts:
                    self.inventory.release_item(item_id, quantity)
                    self.notifier.send_email(user["email"], "Order Failed", f"Payment failed for item {item_id}")
                    raise
        raise PaymentError("Unable to complete payment")

if __name__ == "__main__":
    users = {"alice": {"email": "alice@example.com", "active": True}, "bob": {"email": "bob", "active": True}}
    stock = {"widget": 5}
    auth = AuthService(users)
    inventory = InventoryService(stock)
    payment = PaymentService()
    notifier = NotificationService()
    processor = OrderProcessor(auth, inventory, payment, notifier)

    try:
        result = processor.place_order("alice", "widget", 2, {"number": "4111111111111111"})
        print("Order result:", result)
    except Exception as e:
        print("Order failed:", e)

    try:
        result = processor.place_order("bob", "widget", 1, {"number": "4000000000000000"})
        print("Order result:", result)
    except Exception as e:
        print("Order failed:", e)
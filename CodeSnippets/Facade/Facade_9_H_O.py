import threading
import uuid
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

class AuthError(Exception):
    pass

class InventoryError(Exception):
    pass

class PaymentError(Exception):
    pass

class AuthService:
    def __init__(self, valid_tokens=None):
        self.valid_tokens = valid_tokens or {}

    def authenticate(self, user_id, token):
        expected = self.valid_tokens.get(user_id)
        if expected is None or expected != token:
            raise AuthError("authentication failed")
        return True

class InventoryService:
    def __init__(self, initial_stock=None):
        self.stock = initial_stock or {}
        self.lock = threading.Lock()
        self.reservations = {}

    def reserve(self, item_id, qty):
        with self.lock:
            available = self.stock.get(item_id, 0)
            if qty <= 0:
                raise InventoryError("invalid quantity")
            if available < qty:
                raise InventoryError("insufficient stock")
            self.stock[item_id] = available - qty
            res_id = str(uuid.uuid4())
            self.reservations[res_id] = (item_id, qty)
            return res_id

    def release(self, reservation_id):
        with self.lock:
            entry = self.reservations.pop(reservation_id, None)
            if not entry:
                return False
            item_id, qty = entry
            self.stock[item_id] = self.stock.get(item_id, 0) + qty
            return True

    def commit(self, reservation_id):
        with self.lock:
            if reservation_id not in self.reservations:
                raise InventoryError("invalid reservation")
            self.reservations.pop(reservation_id, None)
            return True

class PaymentService:
    def __init__(self, fail_rate=0.2, transient_rate=0.1):
        self.fail_rate = fail_rate
        self.transient_rate = transient_rate

    def charge(self, user_id, amount):
        if amount <= 0:
            raise PaymentError("invalid amount")
        r = random.random()
        if r < self.transient_rate:
            raise PaymentError("transient network error")
        if r < self.transient_rate + self.fail_rate:
            raise PaymentError("payment declined")
        return str(uuid.uuid4())

class OrderOrchestrator:
    def __init__(self, auth_service, inventory_service, payment_service,
                 max_retries=3, backoff=0.1):
        self.auth = auth_service
        self.inv = inventory_service
        self.pay = payment_service
        self.max_retries = max_retries
        self.backoff = backoff

    def _retry(self, func, *args, **kwargs):
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exc = e
                time.sleep(self.backoff * attempt)
        raise last_exc

    def place_order(self, user_id, token, item_id, qty, amount):
        logging.info("Starting order for user %s", user_id)
        self.auth.authenticate(user_id, token)
        reservation_id = None
        try:
            reservation_id = self._retry(self.inv.reserve, item_id, qty)
            logging.info("Reserved %s x%d -> %s", item_id, qty, reservation_id)
            tx_id = self._retry(self.pay.charge, user_id, amount)
            logging.info("Payment succeeded -> %s", tx_id)
            self.inv.commit(reservation_id)
            logging.info("Order completed: reservation %s committed", reservation_id)
            return {"status": "success", "reservation": reservation_id, "transaction": tx_id}
        except AuthError:
            logging.info("Authentication failed for user %s", user_id)
            raise
        except PaymentError as pe:
            logging.info("Payment failed: %s", pe)
            if reservation_id:
                released = self.inv.release(reservation_id)
                logging.info("Released reservation %s: %s", reservation_id, released)
            raise
        except InventoryError as ie:
            logging.info("Inventory error: %s", ie)
            raise
        except Exception as e:
            logging.info("Unexpected error: %s", e)
            if reservation_id:
                try:
                    self.inv.release(reservation_id)
                except Exception:
                    pass
            raise

if __name__ == "__main__":
    random.seed(42)
    auth = AuthService(valid_tokens={"alice": "token123", "bob": "token456"})
    inventory = InventoryService(initial_stock={"widget": 5})
    payment = PaymentService(fail_rate=0.3, transient_rate=0.1)
    orchestrator = OrderOrchestrator(auth, inventory, payment, max_retries=4, backoff=0.05)

    try:
        result = orchestrator.place_order("alice", "token123", "widget", 2, 49.99)
        print("Order result:", result)
    except Exception as e:
        print("Order failed:", e)

    try:
        result = orchestrator.place_order("bob", "token456", "widget", 4, 99.99)
        print("Order result:", result)
    except Exception as e:
        print("Order failed:", e)

    try:
        result = orchestrator.place_order("eve", "badtoken", "widget", 1, 9.99)
        print("Order result:", result)
    except Exception as e:
        print("Order failed:", e)
import threading
import time
from contextlib import contextmanager

class AuthService:
    _lock = threading.Lock()
    def __init__(self):
        self.sessions = {}
    def login(self, user, pwd):
        with self._lock:
            if user == "admin" and pwd == "s3cr3t":
                token = f"tok_{int(time.time()*1000)}"
                self.sessions[token] = user
                return token
            raise PermissionError("Invalid credentials")
    def logout(self, token):
        with self._lock:
            self.sessions.pop(token, None)

class DataStore:
    _lock = threading.Lock()
    def __init__(self):
        self.db = {"orders": {}, "inventory": {"apple": 10}}
    def reserve_item(self, item, qty):
        with self._lock:
            if self.db["inventory"].get(item, 0) >= qty:
                self.db["inventory"][item] -= qty
                return True
            return False
    def save_order(self, oid, details):
        with self._lock:
            self.db["orders"][oid] = details
    def get_inventory(self):
        with self._lock:
            return dict(self.db["inventory"])

class PaymentGateway:
    def charge(self, token, amount):
        if not token.startswith("tok_"):
            raise ValueError("Bad token")
        return f"pay_{int(time.time()*1000)}"

class NotificationCenter:
    def send_email(self, user, msg):
        pass

class ShopFront:
    def __init__(self):
        self.auth = AuthService()
        self.store = DataStore()
        self.pay = PaymentGateway()
        self.notify = NotificationCenter()
    @contextmanager
    def session(self, user, pwd):
        token = self.auth.login(user, pwd)
        try:
            yield token
        finally:
            self.auth.logout(token)
    def quick_order(self, user, pwd, item, qty):
        with self.session(user, pwd) as token:
            if not self.store.reserve_item(item, qty):
                raise RuntimeError("Out of stock")
            pay_id = self.pay.charge(token, qty * 1.5)
            oid = f"ord_{int(time.time()*1000)}"
            self.store.save_order(oid, {"item": item, "qty": qty, "pay": pay_id})
            self.notify.send_email(user, f"Order {oid} confirmed")
            return oid

if __name__ == "__main__":
    front = ShopFront()
    try:
        order = front.quick_order("admin", "s3cr3t", "apple", 2)
        print("Order placed:", order)
        print("Remaining stock:", front.store.get_inventory())
    except Exception as e:
        print("Error:", e)
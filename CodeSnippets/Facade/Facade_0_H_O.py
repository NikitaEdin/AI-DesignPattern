import threading
import uuid
import time
from dataclasses import dataclass
from typing import Dict, Tuple

class AuthError(Exception): pass
class InsufficientStock(Exception): pass
class PaymentError(Exception): pass
class NotificationError(Exception): pass

class AuthService:
    def __init__(self, valid_tokens):
        self._valid = set(valid_tokens)
    def authenticate(self, token: str) -> bool:
        if token in self._valid:
            return True
        raise AuthError("invalid token")

class InventoryManager:
    def __init__(self, initial_stock: Dict[str, int]):
        self._stock = dict(initial_stock)
        self._reservations: Dict[str, Dict[str,int]] = {}
        self._lock = threading.Lock()
    def reserve(self, items: Dict[str,int]) -> str:
        with self._lock:
            for sku, qty in items.items():
                if self._stock.get(sku, 0) < qty:
                    raise InsufficientStock(sku)
            res_id = str(uuid.uuid4())
            self._reservations[res_id] = dict(items)
            for sku, qty in items.items():
                self._stock[sku] -= qty
            return res_id
    def commit(self, res_id: str) -> None:
        with self._lock:
            self._reservations.pop(res_id, None)
    def release(self, res_id: str) -> None:
        with self._lock:
            items = self._reservations.pop(res_id, {})
            for sku, qty in items.items():
                self._stock[sku] = self._stock.get(sku, 0) + qty

class PaymentGateway:
    def __init__(self):
        self._charges: Dict[str, Dict] = {}
        self._attempts: Dict[str, int] = {}
        self._lock = threading.Lock()
    def process(self, amount: float, card_info: str, idempotency_key: str) -> str:
        with self._lock:
            attempts = self._attempts.get(idempotency_key, 0) + 1
            self._attempts[idempotency_key] = attempts
            if card_info == "bad":
                raise PaymentError("card declined")
            if card_info == "transient" and attempts < 2:
                raise PaymentError("transient gateway error")
            charge_id = str(uuid.uuid4())
            self._charges[charge_id] = {"amount": amount, "card": card_info}
            return charge_id
    def refund(self, charge_id: str) -> bool:
        with self._lock:
            return self._charges.pop(charge_id, None) is not None

class NotificationService:
    def __init__(self):
        self._outbox = []
        self._lock = threading.Lock()
    def send(self, email: str, message: str) -> None:
        if email == "fail@example.com":
            raise NotificationError("smtp down")
        # simulate send latency
        time.sleep(0.01)
    def send_with_retry(self, email: str, message: str, retries: int = 3) -> None:
        for attempt in range(1, retries+1):
            try:
                self.send(email, message)
                return
            except NotificationError:
                time.sleep(0.05 * attempt)
        with self._lock:
            self._outbox.append((email, message))

@dataclass
class OrderResult:
    success: bool
    order_id: str
    charge_id: str = ""
    message: str = ""

class OrderCoordinator:
    def __init__(self, auth: AuthService, inv: InventoryManager, pay: PaymentGateway, note: NotificationService):
        self.auth = auth
        self.inv = inv
        self.pay = pay
        self.note = note
    def place_order(self, order_id: str, user_token: str, items: Dict[str,int], card_info: str, email: str, amount: float) -> OrderResult:
        try:
            self.auth.authenticate(user_token)
            res_id = self.inv.reserve(items)
            try:
                idempotency_key = f"{order_id}:{user_token}:{hash(card_info)}"
                # payment gateway simulates retries/stateful idempotency
                charge_id = None
                for attempt in range(3):
                    try:
                        charge_id = self.pay.process(amount, card_info, idempotency_key)
                        break
                    except PaymentError as e:
                        if attempt == 2:
                            raise
                        time.sleep(0.05 * (attempt+1))
                self.inv.commit(res_id)
                # Notifications are best-effort; failures do not rollback committed transaction
                try:
                    self.note.send_with_retry(email, f"Order {order_id} confirmed. Charge {charge_id}")
                except Exception:
                    pass
                return OrderResult(True, order_id, charge_id, "order completed")
            except PaymentError as pe:
                # refund attempt if charge existed
                if 'charge_id' in locals() and charge_id:
                    try:
                        self.pay.refund(charge_id)
                    except Exception:
                        pass
                self.inv.release(res_id)
                return OrderResult(False, order_id, "", f"payment failed: {pe}")
            except Exception as e:
                self.inv.release(res_id)
                return OrderResult(False, order_id, "", f"order failed: {e}")
        except AuthError as ae:
            return OrderResult(False, order_id, "", f"auth failed: {ae}")
        except InsufficientStock as isx:
            return OrderResult(False, order_id, "", f"stock insufficient: {isx}")
        except Exception as e:
            return OrderResult(False, order_id, "", f"unexpected error: {e}")

if __name__ == "__main__":
    auth = AuthService(valid_tokens=["token123"])
    inv = InventoryManager({"widget": 5, "gizmo": 2})
    pay = PaymentGateway()
    note = NotificationService()
    coord = OrderCoordinator(auth, inv, pay, note)

    # Successful order
    r1 = coord.place_order("ord-1", "token123", {"widget": 2}, "visa", "user@example.com", 49.99)
    print(r1)

    # Transient payment that succeeds on retry
    r2 = coord.place_order("ord-2", "token123", {"gizmo": 1}, "transient", "user2@example.com", 19.99)
    print(r2)

    # Notification failure does not rollback committed order
    r3 = coord.place_order("ord-3", "token123", {"widget": 1}, "visa", "fail@example.com", 9.99)
    print(r3)

    # Payment permanent failure
    r4 = coord.place_order("ord-4", "token123", {"widget": 1}, "bad", "user3@example.com", 9.99)
    print(r4)
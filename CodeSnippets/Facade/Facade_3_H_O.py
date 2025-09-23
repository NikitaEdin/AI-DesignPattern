import threading
import time
import random
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional

class ValidationError(Exception):
    pass

class PaymentError(Exception):
    pass

class OutOfStockError(Exception):
    pass

class OrderProcessingError(Exception):
    pass

@dataclass
class Item:
    sku: str
    quantity: int
    price: float

@dataclass
class Order:
    customer_id: str
    items: List[Item]
    card_info: Dict[str, str]
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict = field(default_factory=dict)

    @property
    def total(self) -> float:
        return sum(i.quantity * i.price for i in self.items)

class AccountValidator:
    def validate(self, customer_id: str, card_info: Dict[str, str]) -> bool:
        if not customer_id or "number" not in card_info:
            raise ValidationError("Invalid customer or card information")
        if len(card_info.get("number", "")) < 12:
            raise ValidationError("Card number too short")
        return True

class PaymentProcessor:
    def __init__(self, fail_rate: float = 0.2, max_retries: int = 3):
        self.fail_rate = fail_rate
        self.max_retries = max_retries

    def charge(self, card_info: Dict[str, str], amount: float, order_id: str) -> Dict:
        delay = 0.1
        for attempt in range(1, self.max_retries + 1):
            if random.random() > self.fail_rate:
                txn_id = f"txn_{uuid.uuid4().hex[:12]}"
                return {"status": "charged", "transaction_id": txn_id, "amount": amount}
            time.sleep(delay)
            delay *= 2
        raise PaymentError(f"Payment failed after {self.max_retries} attempts for order {order_id}")

class InventoryManager:
    def __init__(self, initial_stock: Optional[Dict[str, int]] = None):
        self._stock = dict(initial_stock or {})
        self._lock = threading.Lock()

    def reserve_items(self, items: List[Item]) -> None:
        with self._lock:
            shortages = []
            for it in items:
                avail = self._stock.get(it.sku, 0)
                if avail < it.quantity:
                    shortages.append((it.sku, it.quantity, avail))
            if shortages:
                raise OutOfStockError(f"Out of stock: {shortages}")
            for it in items:
                self._stock[it.sku] = self._stock.get(it.sku, 0) - it.quantity

    def release_items(self, items: List[Item]) -> None:
        with self._lock:
            for it in items:
                self._stock[it.sku] = self._stock.get(it.sku, 0) + it.quantity

    def current_stock(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stock)

class NotificationService:
    def __init__(self, fail_rate: float = 0.1):
        self.fail_rate = fail_rate

    def send(self, customer_id: str, message: str) -> bool:
        if random.random() < self.fail_rate:
            return False
        print(f"Notify {customer_id}: {message}")
        return True

class OrderService:
    def __init__(self, validator: AccountValidator, payment: PaymentProcessor, inventory: InventoryManager, notifier: NotificationService):
        self.validator = validator
        self.payment = payment
        self.inventory = inventory
        self.notifier = notifier
        self._processed_ids = set()
        self._lock = threading.Lock()

    def process_order(self, order: Order, idempotency_key: Optional[str] = None) -> Dict:
        key = idempotency_key or order.order_id
        with self._lock:
            if key in self._processed_ids:
                return {"status": "already_processed", "order_id": order.order_id}
            self._processed_ids.add(key)
        try:
            self.validator.validate(order.customer_id, order.card_info)
            self.inventory.reserve_items(order.items)
            try:
                payment_result = self.payment.charge(order.card_info, order.total, order.order_id)
            except Exception as e:
                self.inventory.release_items(order.items)
                raise
            notified = self.notifier.send(order.customer_id, f"Order {order.order_id} confirmed. Amount: {order.total}")
            return {"status": "completed", "order_id": order.order_id, "payment": payment_result, "notified": notified}
        except Exception as e:
            with self._lock:
                self._processed_ids.discard(key)
            raise OrderProcessingError(str(e)) from e

if __name__ == "__main__":
    random.seed(42)
    validator = AccountValidator()
    payment = PaymentProcessor(fail_rate=0.3, max_retries=4)
    inventory = InventoryManager(initial_stock={"A1": 5, "B2": 2})
    notifier = NotificationService(fail_rate=0.05)
    service = OrderService(validator, payment, inventory, notifier)

    order = Order(
        customer_id="cust_123",
        items=[Item(sku="A1", quantity=2, price=10.0), Item(sku="B2", quantity=1, price=20.0)],
        card_info={"number": "424242424242", "expiry": "12/26"}
    )

    try:
        result = service.process_order(order)
        print("Result:", result)
    except Exception as e:
        print("Processing failed:", e)

    try:
        result2 = service.process_order(order)
        print("Idempotent call result:", result2)
    except Exception as e:
        print("Second processing failed:", e)

    print("Stock after:", inventory.current_stock())
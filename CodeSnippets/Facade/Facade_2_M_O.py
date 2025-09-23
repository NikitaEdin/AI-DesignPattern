import time
import random

class UserDatabase:
    def __init__(self):
        self._users = {}

    def add_user(self, user_id, info):
        if user_id in self._users:
            raise ValueError("User already exists")
        self._users[user_id] = info
        return True

    def remove_user(self, user_id):
        if user_id not in self._users:
            raise KeyError("User not found")
        del self._users[user_id]
        return True

class PaymentProcessor:
    def charge(self, card_number, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        if card_number == "0000-0000-0000-0000":
            raise ConnectionError("Card declined")
        time.sleep(0.1)
        return {"status": "charged", "amount": amount}

    def refund(self, transaction_id):
        time.sleep(0.05)
        return {"status": "refunded", "transaction_id": transaction_id}

class MessageSender:
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts

    def _attempt_send(self, address, payload):
        if random.random() < 0.3:
            raise ConnectionError("Transient send failure")
        return True

    def send(self, address, payload):
        last_error = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self._attempt_send(address, payload)
            except Exception as e:
                last_error = e
                time.sleep(0.05 * attempt)
        raise last_error

class SubscriptionManager:
    def __init__(self, user_db, payments, messenger):
        self.users = user_db
        self.payments = payments
        self.messenger = messenger

    def subscribe(self, user_id, info, card_number, amount):
        try:
            self.users.add_user(user_id, info)
            charge = self.payments.charge(card_number, amount)
            self.messenger.send(info.get("email"), f"Welcome {user_id}")
            self.messenger.send(info.get("email"), f"Receipt: {charge}")
            return {"user": user_id, "status": "subscribed"}
        except Exception as e:
            try:
                self.users.remove_user(user_id)
            except Exception:
                pass
            return {"user": user_id, "status": "failed", "error": str(e)}

    def unsubscribe(self, user_id, transaction_id=None):
        try:
            self.users.remove_user(user_id)
            if transaction_id:
                self.payments.refund(transaction_id)
            return {"user": user_id, "status": "unsubscribed"}
        except Exception as e:
            return {"user": user_id, "status": "failed", "error": str(e)}

if __name__ == "__main__":
    random.seed(1)
    db = UserDatabase()
    payments = PaymentProcessor()
    messenger = MessageSender(max_attempts=4)
    manager = SubscriptionManager(db, payments, messenger)

    result1 = manager.subscribe("alice", {"email": "alice@example.com"}, "1234-5678-9012-3456", 29.99)
    print(result1)

    result2 = manager.subscribe("bob", {"email": "bob@example.com"}, "0000-0000-0000-0000", 29.99)
    print(result2)

    result3 = manager.unsubscribe("alice", transaction_id="tx-1001")
    print(result3)
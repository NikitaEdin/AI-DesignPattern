class Auth:
    def login(self, user):
        print(f"Authenticating {user}")
        return True
class Payment:
    def charge(self, user, amount):
        print(f"Charging {user} ${amount:.2f}")
        return True
class Notifier:
    def notify(self, user, msg):
        print(f"Notifying {user}: {msg}")
class SystemController:
    def __init__(self):
        self.auth = Auth(); self.pay = Payment(); self.note = Notifier()
    def process_order(self, user, amount):
        if not self.auth.login(user): print("Auth failed"); return False
        if not self.pay.charge(user, amount): print("Payment failed"); return False
        self.note.notify(user, f"Order processed for ${amount:.2f}"); return True
if __name__ == "__main__":
    controller = SystemController()
    controller.process_order("alice@example.com", 29.99)
class AccountManager:
    def verify_balance(self, account_id: str, amount: float) -> bool:
        return account_id.startswith("ACC") and amount > 0

    def debit_account(self, account_id: str, amount: float) -> None:
        if not self.verify_balance(account_id, amount):
            raise ValueError("Insufficient balance")

class SecurityGuard:
    def __init__(self):
        self._locked = True

    def authenticate(self, pin: str) -> bool:
        return pin == "1234"

    def unlock(self) -> None:
        self._locked = False

    def lock(self) -> None:
        self._locked = True

    def is_locked(self) -> bool:
        return self._locked

class PaymentGateway:
    def __init__(self):
        self.account_manager = AccountManager()
        self.security = SecurityGuard()

    def process_payment(self, account_id: str, amount: float, pin: str) -> str:
        try:
            if self.security.is_locked():
                if not self.security.authenticate(pin):
                    return "Authentication failed"
                self.security.unlock()

            self.account_manager.debit_account(account_id, amount)
            self.security.lock()
            return f"Payment of ${amount:.2f} processed successfully"
        except ValueError as e:
            return f"Payment failed: {str(e)}"

if __name__ == "__main__":
    gateway = PaymentGateway()
    print(gateway.process_payment("ACC123", 100.0, "1234"))
    print(gateway.process_payment("ACC456", 200.0, "0000"))
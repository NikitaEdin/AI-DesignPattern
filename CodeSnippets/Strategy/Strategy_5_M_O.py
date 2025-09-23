from typing import Protocol, runtime_checkable, Optional

@runtime_checkable
class PaymentMethod(Protocol):
    def pay(self, amount: float) -> str: ...

class CreditCardProcessor:
    def pay(self, amount: float) -> str:
        # simulate decline for large amounts
        if amount > 500:
            raise RuntimeError("Declined by issuer")
        return f"Charged ${amount:.2f} to credit card"

class PayPalProcessor:
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal"

class BankTransferProcessor:
    def pay(self, amount: float) -> str:
        if amount > 1000:
            raise RuntimeError("Insufficient funds in bank account")
        return f"Transferred ${amount:.2f} by bank transfer"

class TransactionManager:
    def __init__(self, primary: PaymentMethod, fallback: Optional[PaymentMethod] = None, attempts: int = 1):
        if not isinstance(primary, PaymentMethod):
            raise TypeError("Primary must implement the payment interface")
        if fallback is not None and not isinstance(fallback, PaymentMethod):
            raise TypeError("Fallback must implement the payment interface")
        self.primary = primary
        self.fallback = fallback
        self.attempts = max(1, int(attempts))

    def set_primary(self, handler: PaymentMethod) -> None:
        if not isinstance(handler, PaymentMethod):
            raise TypeError("Primary must implement the payment interface")
        self.primary = handler

    def set_fallback(self, handler: Optional[PaymentMethod]) -> None:
        if handler is not None and not isinstance(handler, PaymentMethod):
            raise TypeError("Fallback must implement the payment interface")
        self.fallback = handler

    def process(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        last_error: Optional[Exception] = None
        for attempt in range(self.attempts):
            try:
                return self.primary.pay(amount)
            except Exception as e:
                last_error = e
                if attempt < self.attempts - 1:
                    continue
                if self.fallback is not None:
                    try:
                        return self.fallback.pay(amount)
                    except Exception as fe:
                        raise RuntimeError(f"Primary and fallback failed: {last_error}") from fe
                raise RuntimeError(f"Primary failed: {last_error}") from last_error

if __name__ == "__main__":
    primary = CreditCardProcessor()
    fallback = PayPalProcessor()
    manager = TransactionManager(primary=primary, fallback=fallback, attempts=3)

    print(manager.process(100.0))   # expected primary success
    print(manager.process(600.0))   # expected primary fail, fallback succeeds

    # swap primary at runtime
    manager.set_primary(BankTransferProcessor())
    try:
        print(manager.process(1200.0))  # primary fails, fallback used
    except RuntimeError as err:
        print("Transaction failed:", err)
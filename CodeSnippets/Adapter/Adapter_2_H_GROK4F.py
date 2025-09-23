from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class ModernProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        print(f"Processing modern payment of {amount}")
        return True

class LegacyWireTransfer:
    def wire_money(self, amount: float, recipient: str) -> bool:
        print(f"Wiring {amount} to {recipient}")
        if amount > 10000:
            raise RuntimeError("Transfer limit exceeded")
        return True

class LegacyCheckWriter:
    def issue_check(self, amount: float) -> bool:
        print(f"Issuing check for {amount}")
        return True

class WirePaymentProcessor(PaymentProcessor):
    def __init__(self, wire_service: LegacyWireTransfer, default_recipient: str = "DEFAULT"):
        self.wire_service = wire_service
        self.default_recipient = default_recipient
        self._transaction_log = []

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Invalid amount")
        try:
            success = self.wire_service.wire_money(amount, self.default_recipient)
            if success:
                self._transaction_log.append({"amount": amount, "recipient": self.default_recipient})
                print(f"Transaction logged: {amount}")
            return success
        except Exception as e:
            print(f"Error in wire transfer: {e}")
            return False

    def get_transaction_count(self) -> int:
        return len(self._transaction_log)

class CheckPaymentProcessor(PaymentProcessor):
    def __init__(self, check_service: LegacyCheckWriter):
        self.check_service = check_service
        self._failed_attempts = 0

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Invalid amount")
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                return self.check_service.issue_check(amount)
            except Exception:
                self._failed_attempts += 1
                if attempt < max_retries:
                    print(f"Retry {attempt + 1} for check issuance")
                else:
                    print("Max retries exceeded for check")
                    return False
        return False

if __name__ == "__main__":
    modern = ModernProcessor()
    print("Modern payment result:", modern.process_payment(100.0))

    wire_service = LegacyWireTransfer()
    wire_processor = WirePaymentProcessor(wire_service, "BankAccount123")
    print("Wire payment result:", wire_processor.process_payment(200.0))
    print("Transaction count:", wire_processor.get_transaction_count())

    try:
        wire_processor.process_payment(-10.0)
    except ValueError as e:
        print("Error:", e)

    try:
        wire_processor.process_payment(15000.0)
    except RuntimeError as e:
        print("Error:", e)

    check_service = LegacyCheckWriter()
    check_processor = CheckPaymentProcessor(check_service)
    print("Check payment result:", check_processor.process_payment(50.0))
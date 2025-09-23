class PaymentService:
    def process_payment(self, amount: float, currency: str) -> bool:
        raise NotImplementedError("Subclasses must implement process_payment")

class ModernPaymentGateway(PaymentService):
    def process_payment(self, amount: float, currency: str) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        print(f"Processing modern payment: {amount:.2f} {currency}")
        return True

class LegacyBank:
    def __init__(self):
        self.supported_currencies = ["USD"]
        self.min_transfer = 0.01

    def transfer_funds(self, account_number: str, amount_in_usd: float) -> bool:
        if not account_number or len(account_number) < 5:
            raise ValueError("Invalid account number")
        if amount_in_usd < self.min_transfer:
            raise ValueError("Amount below minimum transfer limit")
        if amount_in_usd > 10000:  # Simulate daily limit
            raise ValueError("Transfer exceeds daily limit")
        print(f"Legacy bank transfer: {amount_in_usd:.2f} USD to account {account_number}")
        return True

class BankPaymentBridge(PaymentService):
    def __init__(self, bank: LegacyBank, account_number: str):
        if not isinstance(bank, LegacyBank):
            raise TypeError("Must provide a LegacyBank instance")
        self.bank = bank
        self.account_number = account_number
        self.currency_rates = {
            "USD": 1.0,
            "EUR": 0.85,  # Simplified rate to USD
            "GBP": 1.25,
            "JPY": 0.007
        }

    def process_payment(self, amount: float, currency: str) -> bool:
        if amount <= 0:
            print(f"Payment rejected: Invalid amount {amount}")
            return False
        if currency not in self.currency_rates:
            print(f"Payment failed: Unsupported currency {currency}")
            return False
        try:
            usd_amount = amount / self.currency_rates[currency]
            return self.bank.transfer_funds(self.account_number, usd_amount)
        except ValueError as e:
            print(f"Payment bridge error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error in payment bridge: {e}")
            return False

if __name__ == "__main__":
    modern_gateway = ModernPaymentGateway()
    success_modern = modern_gateway.process_payment(150.0, "USD")
    print(f"Modern payment success: {success_modern}\n")

    legacy_bank = LegacyBank()
    payment_bridge = BankPaymentBridge(legacy_bank, "ACC12345")

    success_eur = payment_bridge.process_payment(100.0, "EUR")
    print(f"EUR payment via bridge success: {success_eur}\n")

    failure_small = payment_bridge.process_payment(0.001, "USD")
    print(f"Small amount failure: {failure_small}\n")

    failure_large = payment_bridge.process_payment(20000.0, "USD")
    print(f"Large amount failure: {failure_large}\n")

    failure_invalid_currency = payment_bridge.process_payment(50.0, "XYZ")
    print(f"Invalid currency failure: {failure_invalid_currency}\n")

    invalid_bridge = BankPaymentBridge(ModernPaymentGateway(), "INVALID")
    try:
        invalid_bridge.process_payment(10.0, "USD")
    except TypeError as e:
        print(f"Type error in bridge init: {e}")
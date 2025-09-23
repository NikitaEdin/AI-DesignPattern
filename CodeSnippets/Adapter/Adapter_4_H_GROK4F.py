from abc import ABC, abstractmethod
import sys

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> bool:
        pass

class SimpleBank(PaymentProcessor):
    def process_payment(self, amount: float, currency: str) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        currency = currency.upper()
        if currency not in ['USD', 'EUR']:
            raise ValueError("Unsupported currency")
        print(f"SimpleBank processed {amount:.2f} {currency}")
        return True

class PayPalService:
    def make_payment(self, amount_cents: int) -> bool:
        if amount_cents <= 0 or amount_cents > 10000000:
            print("PayPal rejected payment: invalid amount")
            return False
        usd_amount = amount_cents / 100
        print(f"PayPal processed {usd_amount:.2f} USD")
        return True

class PayPalProcessor(PaymentProcessor):
    def __init__(self, paypal_service: PayPalService):
        self.paypal = paypal_service
        self.exchange_rates = {
            'USD': 1.0,
            'EUR': 1.08,
            'GBP': 1.27
        }

    def process_payment(self, amount: float, currency: str) -> bool:
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        currency = currency.upper().strip()
        if currency not in self.exchange_rates:
            raise ValueError(f"Unsupported currency: {currency}")
        try:
            usd_amount = amount * self.exchange_rates[currency]
            amount_cents = int(round(usd_amount * 100))
            print(f"Converted {amount:.2f} {currency} to {usd_amount:.2f} USD")
            return self.paypal.make_payment(amount_cents)
        except Exception as e:
            print(f"Conversion error: {e}")
            return False

if __name__ == "__main__":
    bank = SimpleBank()
    success = bank.process_payment(100.0, "USD")
    print(f"Bank payment success: {success}\n")

    paypal = PayPalService()
    compat_paypal = PayPalProcessor(paypal)
    success = compat_paypal.process_payment(50.0, "EUR")
    print(f"PayPal (EUR) success: {success}\n")

    success = compat_paypal.process_payment(75.5, "GBP")
    print(f"PayPal (GBP) success: {success}\n")

    try:
        compat_paypal.process_payment(-10.0, "USD")
    except ValueError as e:
        print(f"Error: {e}\n")

    success = compat_paypal.process_payment(100000.0, "USD")
    print(f"Large PayPal success: {success}")
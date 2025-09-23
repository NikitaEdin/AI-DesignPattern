from abc import ABC, abstractmethod
from typing import Dict, Any

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> bool:
        pass

class StripeGateway:
    def __init__(self):
        self._exchange_rates: Dict[str, float] = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73
        }

    def charge(self, amount_cents: int) -> bool:
        if amount_cents <= 0:
            return False
        # Simulate charge processing
        print(f"Charging {amount_cents} cents via Stripe")
        return True

class StripePaymentHandler(PaymentProcessor):
    def __init__(self, gateway: StripeGateway):
        self._gateway = gateway

    def process_payment(self, amount: float, currency: str) -> bool:
        try:
            if amount <= 0:
                print("Invalid amount: must be positive")
                return False
            if currency not in self._gateway._exchange_rates:
                raise ValueError(f"Unsupported currency: {currency}")
            
            rate = self._gateway._exchange_rates[currency]
            usd_amount = amount * rate
            amount_cents = int(usd_amount * 100 + 0.5)  # Round to nearest cent
            
            success = self._gateway.charge(amount_cents)
            if success:
                print(f"Payment of {amount} {currency} processed successfully")
            else:
                print("Payment failed")
            return success
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

if __name__ == "__main__":
    gateway = StripeGateway()
    handler = StripePaymentHandler(gateway)
    
    # Successful payment
    handler.process_payment(100.0, 'USD')
    
    # Edge case: invalid amount
    handler.process_payment(-50.0, 'EUR')
    
    # Edge case: unsupported currency
    handler.process_payment(200.0, 'JPY')
    
    # Another successful
    handler.process_payment(75.5, 'GBP')
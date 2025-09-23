from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        if amount <= 0:
            logging.error("Invalid amount for credit card: %f", amount)
            return False
        fee = amount * 0.03
        total = amount + fee
        logging.info("Processing credit card payment: $%f (fee: $%f)", amount, fee)
        return True

class PayPalPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        if amount <= 0:
            logging.error("Invalid amount for PayPal: %f", amount)
            return False
        if amount > 10000:
            logging.error("Amount too large for PayPal: %f", amount)
            return False
        logging.info("Processing PayPal payment: $%f", amount)
        return True

class BankTransferPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        if amount <= 0:
            logging.error("Invalid amount for bank transfer: %f", amount)
            return False
        delay = "3-5 business days"
        logging.info("Initiating bank transfer: $%f (expected in %s)", amount, delay)
        return True

class OrderProcessor:
    def __init__(self):
        self._method = None

    def set_payment_method(self, method: PaymentMethod):
        if not isinstance(method, PaymentMethod):
            raise ValueError("Invalid payment method provided")
        self._method = method
        logging.info("Payment method set to: %s", type(method).__name__)

    def process_order(self, amount: float) -> bool:
        if self._method is None:
            logging.error("No payment method selected")
            return False
        if amount <= 0:
            logging.error("Order amount must be positive: %f", amount)
            return False
        return self._method.process(amount)

if __name__ == "__main__":
    processor = OrderProcessor()
    
    credit = CreditCardPayment()
    processor.set_payment_method(credit)
    processor.process_order(100.0)
    
    invalid = processor.process_order(-50.0)
    assert not invalid
    
    paypal = PayPalPayment()
    processor.set_payment_method(paypal)
    processor.process_order(200.0)
    
    large = processor.process_order(15000.0)
    assert not large
    
    bank = BankTransferPayment()
    processor.set_payment_method(bank)
    processor.process_order(300.0)
    
    no_method = OrderProcessor()
    no_method.process_order(100.0)
    assert not no_method.process_order(100.0)
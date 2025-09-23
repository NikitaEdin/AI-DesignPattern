from abc import ABC, abstractmethod
import logging

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount, currency):
        pass

class ModernGateway(PaymentProcessor):
    def process_payment(self, amount, currency):
        if amount is None or currency is None:
            raise ValueError("Amount and currency are required")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        print(f"Processed {amount:.2f} {currency} through modern gateway")

class LegacyBankInterface:
    def __init__(self):
        self.supported_currencies = {'EUR', 'GBP', 'USD'}
        self.exchange_rates = {'EUR': 1.08, 'GBP': 1.25, 'USD': 1.0}

    def execute_transfer(self, account, usd_amount):
        if usd_amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if not account:
            raise ValueError("Account is required")
        print(f"Executed bank transfer of {usd_amount:.2f} USD to {account}")

class BankTransactionHandler(PaymentProcessor):
    def __init__(self, bank_interface=None):
        self.bank = bank_interface or LegacyBankInterface()
        self.logger = logging.getLogger("BankHandler")
        self.default_account = "primary_client_account"

    def process_payment(self, amount, currency):
        if amount is None or currency is None:
            raise ValueError("Amount and currency are required")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        currency = currency.upper()
        if currency not in self.bank.supported_currencies:
            raise ValueError(f"Unsupported currency: {currency}")
        try:
            rate = self.bank.exchange_rates[currency]
            usd_amount = amount * rate
            self.bank.execute_transfer(self.default_account, usd_amount)
            self.logger.info(f"Successfully processed {amount:.2f} {currency} ({usd_amount:.2f} USD)")
        except ValueError as e:
            self.logger.error(f"Transaction failed: {e}")
            raise

class PaymentService:
    def __init__(self):
        self.handler = None

    def initiate_payment(self, amount, currency):
        currency = currency.upper()
        if currency in {'USD'}:
            self.handler = ModernGateway()
        elif currency in {'EUR', 'GBP'}:
            self.handler = BankTransactionHandler()
        else:
            raise ValueError(f"Payment service does not support {currency}")
        self.handler.process_payment(amount, currency)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = PaymentService()
    try:
        service.initiate_payment(100.0, "EUR")
        service.initiate_payment(50.0, "USD")
        service.initiate_payment(75.0, "GBP")
        service.initiate_payment(-10.0, "EUR")
    except ValueError as e:
        print(f"Error: {e}")
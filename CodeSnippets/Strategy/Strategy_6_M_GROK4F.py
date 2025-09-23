class PaymentProcessor:
    def __init__(self, processor):
        self.processor = processor

    def process(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return self.processor.execute(amount)

class CreditCardHandler:
    def execute(self, amount):
        return f"Processed {amount} via credit card"

class PayPalHandler:
    def execute(self, amount):
        return f"Processed {amount} via PayPal"

class BankTransferHandler:
    def execute(self, amount):
        return f"Processed {amount} via bank transfer"

if __name__ == "__main__":
    card = CreditCardHandler()
    paypal = PayPalHandler()
    bank = BankTransferHandler()

    processor = PaymentProcessor(card)
    print(processor.process(100))

    processor.processor = paypal
    print(processor.process(50))

    processor.processor = bank
    print(processor.process(200))
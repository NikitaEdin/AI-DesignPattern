class CreditCardProcessor:
    def charge(self, amount):
        return f"Charged ${amount} to credit card"

class PaymentProcessor:
    def __init__(self, card_processor):
        self.card_processor = card_processor

    def process_payment(self, amount):
        return self.card_processor.charge(amount)

if __name__ == "__main__":
    card = CreditCardProcessor()
    processor = PaymentProcessor(card)
    result = processor.process_payment(100)
    print(result)
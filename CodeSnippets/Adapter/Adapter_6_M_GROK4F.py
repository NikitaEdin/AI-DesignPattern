class PaymentProcessor:
    def process_payment(self, amount: float) -> str:
        raise NotImplementedError("Subclasses must implement process_payment")

class BankService:
    def execute_transaction(self, card_details: str, amount: float) -> bool:
        # Simulate transaction: succeed if amount > 0 and card is valid
        if amount <= 0 or not card_details:
            return False
        return True  # Simplified success logic

class BankPaymentHandler(PaymentProcessor):
    def __init__(self, bank_service: BankService, card_details: str):
        self.bank_service = bank_service
        self.card_details = card_details

    def process_payment(self, amount: float) -> str:
        if amount <= 0:
            return "failed: Invalid amount"
        try:
            success = self.bank_service.execute_transaction(self.card_details, amount)
            return "success" if success else "failed: Transaction declined"
        except Exception as e:
            return f"failed: Error processing - {str(e)}"

if __name__ == "__main__":
    bank = BankService()
    handler = BankPaymentHandler(bank, "Visa-1234")
    
    result1 = handler.process_payment(100.0)
    print(f"Payment of 100: {result1}")
    
    result2 = handler.process_payment(0.0)
    print(f"Payment of 0: {result2}")
    
    handler.card_details = ""  # Simulate invalid card
    result3 = handler.process_payment(50.0)
    print(f"Payment of 50 with invalid card: {result3}")
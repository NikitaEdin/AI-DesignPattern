from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class ModernPaymentInterface(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        pass

class LegacyPaymentSystem:
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.transaction_log = []
    
    def make_payment(self, dollars: float, card_number: str):
        if dollars <= 0:
            return f"ERROR: Invalid amount"
        transaction_id = f"TXN_{len(self.transaction_log) + 1:04d}"
        result = f"SUCCESS:{transaction_id}:${dollars:.2f}"
        self.transaction_log.append(result)
        return result
    
    def check_card(self, card_number: str):
        return len(card_number) >= 16 and card_number.isdigit()

class AnotherLegacySystem:
    def __init__(self):
        self.processed_amounts = []
    
    def execute_transfer(self, amount_cents: int, account: str):
        if amount_cents < 100:
            raise ValueError("Minimum transaction is $1.00")
        self.processed_amounts.append(amount_cents)
        return {"status": "completed", "reference": f"REF{sum(self.processed_amounts)}"}

class PaymentBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy_system = legacy_system
        self.currency_rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.73}
    
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not self.validate_transaction({"amount": amount, "currency": currency}):
                return {"success": False, "error": "Validation failed"}
            
            usd_amount = amount / self.currency_rates.get(currency, 1.0)
            card_number = metadata.get("card_number", "1234567890123456")
            
            result = self.legacy_system.make_payment(usd_amount, card_number)
            
            if result.startswith("SUCCESS"):
                parts = result.split(":")
                return {
                    "success": True,
                    "transaction_id": parts[1],
                    "amount": amount,
                    "currency": currency,
                    "converted_amount": usd_amount
                }
            else:
                return {"success": False, "error": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def validate_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        amount = transaction_data.get("amount", 0)
        currency = transaction_data.get("currency", "")
        return amount > 0 and currency in self.currency_rates

class TransferBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: AnotherLegacySystem):
        self.legacy_system = legacy_system
        self.currency_rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.73}
    
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not self.validate_transaction({"amount": amount, "currency": currency}):
                return {"success": False, "error": "Validation failed"}
            
            usd_amount = amount / self.currency_rates.get(currency, 1.0)
            amount_cents = int(usd_amount * 100)
            account = metadata.get("account", "DEFAULT_ACCOUNT")
            
            result = self.legacy_system.execute_transfer(amount_cents, account)
            
            return {
                "success": True,
                "transaction_id": result["reference"],
                "amount": amount,
                "currency": currency,
                "status": result["status"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def validate_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        amount = transaction_data.get("amount", 0)
        currency = transaction_data.get("currency", "")
        usd_amount = amount / self.currency_rates.get(currency, 1.0)
        return amount > 0 and currency in self.currency_rates and usd_amount >= 1.0

class UnifiedPaymentProcessor:
    def __init__(self):
        self.processors: List[ModernPaymentInterface] = []
    
    def add_processor(self, processor: ModernPaymentInterface):
        self.processors.append(processor)
    
    def process_with_fallback(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        for processor in self.processors:
            result = processor.process_payment(amount, currency, metadata)
            if result.get("success"):
                return result
        return {"success": False, "error": "All processors failed"}

if __name__ == "__main__":
    legacy_payment = LegacyPaymentSystem("OldBank")
    legacy_transfer = AnotherLegacySystem()
    
    payment_bridge = PaymentBridge(legacy_payment)
    transfer_bridge = TransferBridge(legacy_transfer)
    
    unified_processor = UnifiedPaymentProcessor()
    unified_processor.add_processor(payment_bridge)
    unified_processor.add_processor(transfer_bridge)
    
    test_cases = [
        (100.0, "USD", {"card_number": "4111111111111111"}),
        (85.0, "EUR", {"account": "ACC123"}),
        (0.50, "USD", {"card_number": "1234567890123456"})
    ]
    
    for amount, currency, metadata in test_cases:
        result = unified_processor.process_with_fallback(amount, currency, metadata)
        print(f"Payment ${amount} {currency}: {json.dumps(result, indent=2)}")
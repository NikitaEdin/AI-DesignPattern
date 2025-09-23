from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json

class ModernPaymentInterface(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        pass

class LegacyPaymentSystem:
    def __init__(self):
        self.transactions = {}
        self.counter = 1000
    
    def charge_card(self, card_number: str, amount_cents: int, customer_name: str) -> str:
        if not card_number or amount_cents <= 0:
            return "ERROR_INVALID_INPUT"
        
        transaction_ref = f"TXN_{self.counter}"
        self.counter += 1
        
        if card_number.startswith("4111"):
            self.transactions[transaction_ref] = "SUCCESS"
        else:
            self.transactions[transaction_ref] = "FAILED"
        
        return transaction_ref
    
    def check_status(self, ref: str) -> str:
        return self.transactions.get(ref, "NOT_FOUND")

class PaymentBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy_system = legacy_system
        self._transaction_cache: Dict[str, Dict[str, Any]] = {}
    
    def process_payment(self, amount: float, currency: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            if currency != "USD":
                raise ValueError("Only USD supported")
            
            card_number = customer_data.get("card_number", "")
            customer_name = customer_data.get("name", "")
            
            if not card_number or not customer_name:
                raise ValueError("Card number and customer name required")
            
            amount_cents = int(amount * 100)
            transaction_ref = self.legacy_system.charge_card(card_number, amount_cents, customer_name)
            
            if transaction_ref.startswith("ERROR"):
                raise RuntimeError(f"Payment processing failed: {transaction_ref}")
            
            result = {
                "transaction_id": transaction_ref,
                "amount": amount,
                "currency": currency,
                "status": "pending",
                "customer": customer_name
            }
            
            self._transaction_cache[transaction_ref] = result.copy()
            return result
            
        except Exception as e:
            return {
                "transaction_id": None,
                "amount": amount,
                "currency": currency,
                "status": "error",
                "error_message": str(e)
            }
    
    def get_transaction_status(self, transaction_id: str) -> str:
        if not transaction_id:
            return "invalid_id"
        
        legacy_status = self.legacy_system.check_status(transaction_id)
        
        status_mapping = {
            "SUCCESS": "completed",
            "FAILED": "declined",
            "NOT_FOUND": "not_found"
        }
        
        mapped_status = status_mapping.get(legacy_status, "unknown")
        
        if transaction_id in self._transaction_cache:
            self._transaction_cache[transaction_id]["status"] = mapped_status
        
        return mapped_status

class ModernPaymentProcessor:
    def __init__(self, payment_interface: ModernPaymentInterface):
        self.payment_interface = payment_interface
    
    def execute_transaction(self, amount: float, currency: str, customer_data: Dict[str, Any]) -> bool:
        result = self.payment_interface.process_payment(amount, currency, customer_data)
        
        if result["status"] == "error":
            print(f"Transaction failed: {result.get('error_message')}")
            return False
        
        transaction_id = result["transaction_id"]
        final_status = self.payment_interface.get_transaction_status(transaction_id)
        
        print(f"Transaction {transaction_id}: {final_status}")
        return final_status == "completed"

if __name__ == "__main__":
    legacy_system = LegacyPaymentSystem()
    bridge = PaymentBridge(legacy_system)
    processor = ModernPaymentProcessor(bridge)
    
    test_customers = [
        {"card_number": "4111111111111111", "name": "Alice Johnson"},
        {"card_number": "5555555555554444", "name": "Bob Smith"},
        {"card_number": "", "name": "Invalid User"}
    ]
    
    for customer in test_customers:
        success = processor.execute_transaction(99.99, "USD", customer)
        print(f"Payment for {customer.get('name', 'Unknown')}: {'✓' if success else '✗'}")
        print("-" * 40)
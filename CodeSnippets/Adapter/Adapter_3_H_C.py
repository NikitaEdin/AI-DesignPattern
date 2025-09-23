from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class ModernPaymentInterface(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_transaction_status(self) -> str:
        pass

class LegacyBankSystem:
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.last_transaction_id = None
        self.transaction_log = []
    
    def make_bank_transfer(self, dollars: int, cents: int):
        transaction_id = f"TXN_{len(self.transaction_log) + 1:06d}"
        total_amount = dollars + (cents / 100)
        
        self.transaction_log.append({
            'id': transaction_id,
            'amount_dollars': dollars,
            'amount_cents': cents,
            'status': 'completed' if total_amount <= 10000 else 'pending'
        })
        self.last_transaction_id = transaction_id
        return transaction_id
    
    def check_transfer_result(self, transaction_id: str):
        for txn in self.transaction_log:
            if txn['id'] == transaction_id:
                return f"BANK_STATUS_{txn['status'].upper()}"
        return "BANK_STATUS_NOT_FOUND"

class ThirdPartyPaymentGateway:
    def __init__(self, gateway_name: str):
        self.gateway_name = gateway_name
        self.processed_amounts = []
    
    def execute_transaction(self, amount_in_cents: int, region_code: str = "US"):
        success = amount_in_cents <= 500000
        self.processed_amounts.append({
            'cents': amount_in_cents,
            'region': region_code,
            'success': success
        })
        return {
            'gateway_response': 'APPROVED' if success else 'DECLINED',
            'reference': f"REF_{len(self.processed_amounts)}"
        }

class BankSystemBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: LegacyBankSystem):
        self._legacy_system = legacy_system
        self._current_transaction_id = None
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        if currency != "USD":
            raise ValueError(f"Unsupported currency: {currency}")
        
        dollars = int(amount)
        cents = int((amount - dollars) * 100)
        
        self._current_transaction_id = self._legacy_system.make_bank_transfer(dollars, cents)
        
        return {
            'transaction_id': self._current_transaction_id,
            'amount': amount,
            'currency': currency,
            'processor': self._legacy_system.bank_name
        }
    
    def get_transaction_status(self) -> str:
        if not self._current_transaction_id:
            return "no_transaction"
        
        bank_status = self._legacy_system.check_transfer_result(self._current_transaction_id)
        status_mapping = {
            'BANK_STATUS_COMPLETED': 'success',
            'BANK_STATUS_PENDING': 'processing',
            'BANK_STATUS_NOT_FOUND': 'error'
        }
        return status_mapping.get(bank_status, 'unknown')

class GatewayBridge(ModernPaymentInterface):
    def __init__(self, gateway: ThirdPartyPaymentGateway):
        self._gateway = gateway
        self._last_response = None
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        amount_in_cents = int(amount * 100)
        
        self._last_response = self._gateway.execute_transaction(amount_in_cents)
        
        return {
            'transaction_id': self._last_response['reference'],
            'amount': amount,
            'currency': currency,
            'processor': self._gateway.gateway_name
        }
    
    def get_transaction_status(self) -> str:
        if not self._last_response:
            return "no_transaction"
        
        return 'success' if self._last_response['gateway_response'] == 'APPROVED' else 'failed'

class PaymentProcessor:
    def __init__(self):
        self.processors: List[ModernPaymentInterface] = []
    
    def add_processor(self, processor: ModernPaymentInterface):
        self.processors.append(processor)
    
    def process_with_fallback(self, amount: float) -> Dict[str, Any]:
        for processor in self.processors:
            try:
                result = processor.process_payment(amount)
                status = processor.get_transaction_status()
                
                if status in ['success', 'processing']:
                    return {**result, 'final_status': status}
                    
            except Exception as e:
                continue
        
        return {'error': 'All processors failed', 'final_status': 'failed'}

if __name__ == "__main__":
    legacy_bank = LegacyBankSystem("National Bank")
    gateway = ThirdPartyPaymentGateway("FastPay")
    
    bank_bridge = BankSystemBridge(legacy_bank)
    gateway_bridge = GatewayBridge(gateway)
    
    payment_system = PaymentProcessor()
    payment_system.add_processor(gateway_bridge)
    payment_system.add_processor(bank_bridge)
    
    test_amounts = [150.75, 6000.00]
    
    for amount in test_amounts:
        print(f"\nProcessing ${amount}")
        result = payment_system.process_with_fallback(amount)
        print(f"Result: {json.dumps(result, indent=2)}")
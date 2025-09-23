from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json

class ModernPaymentInterface(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        pass

class LegacyPaymentSystem:
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.transactions = {}
    
    def make_payment(self, amount_cents: int, card_number: str) -> str:
        if amount_cents <= 0:
            return "FAILED|Invalid amount"
        
        tx_id = f"legacy_{len(self.transactions) + 1}"
        self.transactions[tx_id] = {
            'amount_cents': amount_cents,
            'card': card_number,
            'status': 'SUCCESS' if amount_cents < 1000000 else 'FAILED'
        }
        status = self.transactions[tx_id]['status']
        return f"{status}|{tx_id}"
    
    def check_payment(self, tx_id: str) -> str:
        if tx_id not in self.transactions:
            return "NOT_FOUND"
        return self.transactions[tx_id]['status']

class PaymentBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: LegacyPaymentSystem, conversion_rate: float = 100.0):
        self._legacy_system = legacy_system
        self._conversion_rate = conversion_rate
        self._transaction_mapping = {}
    
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if currency.upper() != 'USD':
                raise ValueError(f"Unsupported currency: {currency}")
            
            card_number = metadata.get('card_number', 'XXXX-XXXX-XXXX-0000')
            amount_cents = int(amount * self._conversion_rate)
            
            legacy_response = self._legacy_system.make_payment(amount_cents, card_number)
            status, transaction_id = legacy_response.split('|', 1)
            
            modern_tx_id = f"modern_{len(self._transaction_mapping) + 1}"
            self._transaction_mapping[modern_tx_id] = transaction_id
            
            return {
                'transaction_id': modern_tx_id,
                'status': 'completed' if status == 'SUCCESS' else 'failed',
                'amount': amount,
                'currency': currency,
                'processed_by': self._legacy_system.system_name
            }
        
        except Exception as e:
            return {
                'transaction_id': None,
                'status': 'error',
                'error': str(e),
                'amount': amount,
                'currency': currency
            }
    
    def get_transaction_status(self, transaction_id: str) -> str:
        if transaction_id not in self._transaction_mapping:
            return 'not_found'
        
        legacy_tx_id = self._transaction_mapping[transaction_id]
        legacy_status = self._legacy_system.check_payment(legacy_tx_id)
        
        status_map = {
            'SUCCESS': 'completed',
            'FAILED': 'failed',
            'NOT_FOUND': 'not_found'
        }
        
        return status_map.get(legacy_status, 'unknown')

class PaymentProcessor:
    def __init__(self, payment_interface: ModernPaymentInterface):
        self.payment_interface = payment_interface
    
    def execute_payment(self, amount: float, currency: str = 'USD', **kwargs) -> Optional[str]:
        result = self.payment_interface.process_payment(amount, currency, kwargs)
        
        if result['status'] == 'completed':
            return result['transaction_id']
        else:
            print(f"Payment failed: {result.get('error', 'Unknown error')}")
            return None

if __name__ == "__main__":
    legacy_system = LegacyPaymentSystem("OldBank_v2.1")
    
    bridge = PaymentBridge(legacy_system)
    processor = PaymentProcessor(bridge)
    
    tx_id = processor.execute_payment(
        amount=99.99,
        currency='USD',
        card_number='4532-1234-5678-9012',
        customer_id='CUST_001'
    )
    
    if tx_id:
        print(f"Payment successful! Transaction ID: {tx_id}")
        status = bridge.get_transaction_status(tx_id)
        print(f"Transaction status: {status}")
    
    large_tx_id = processor.execute_payment(amount=15000.00, card_number='4532-9999-8888-7777')
    if large_tx_id:
        print(f"Large payment status: {bridge.get_transaction_status(large_tx_id)}")
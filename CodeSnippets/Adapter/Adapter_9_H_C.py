from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
import json

class ModernPaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        pass

class LegacyBankSystem:
    def __init__(self, bank_code: str):
        self.bank_code = bank_code
        self.transaction_log = []
    
    def charge_account(self, account_num: str, cents: int, memo: str = "") -> str:
        transaction_id = f"TXN_{len(self.transaction_log) + 1:06d}"
        self.transaction_log.append({
            'id': transaction_id,
            'account': account_num,
            'amount_cents': cents,
            'memo': memo,
            'status': 'SUCCESS' if cents > 0 else 'FAILED'
        })
        return transaction_id
    
    def get_transaction_status(self, txn_id: str) -> str:
        for txn in self.transaction_log:
            if txn['id'] == txn_id:
                return txn['status']
        return 'NOT_FOUND'

class ThirdPartyService:
    @staticmethod
    def validate_card(card_number: str) -> bool:
        return len(card_number) >= 13 and card_number.isdigit()
    
    @staticmethod
    def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
        rates = {'USD': 1.0, 'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0}
        if from_curr not in rates or to_curr not in rates:
            raise ValueError(f"Unsupported currency conversion: {from_curr} to {to_curr}")
        return amount * rates[to_curr] / rates[from_curr]

class PaymentBridge(ModernPaymentProcessor):
    def __init__(self, legacy_system: LegacyBankSystem):
        self._legacy_system = legacy_system
        self._supported_currencies = {'USD', 'EUR', 'GBP', 'JPY'}
    
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        try:
            if not self._validate_input(amount, currency, card_data):
                return self._create_error_response("Invalid input parameters")
            
            if not ThirdPartyService.validate_card(card_data['number']):
                return self._create_error_response("Invalid card number")
            
            converted_amount = self._convert_to_base_currency(amount, currency)
            cents = int(converted_amount * 100)
            
            memo = f"Card ending {card_data['number'][-4:]} - {currency} {amount}"
            transaction_id = self._legacy_system.charge_account(
                card_data['number'], cents, memo
            )
            
            status = self._legacy_system.get_transaction_status(transaction_id)
            
            return {
                'success': status == 'SUCCESS',
                'transaction_id': transaction_id,
                'amount': amount,
                'currency': currency,
                'processed_amount_usd': converted_amount,
                'status': status,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            return self._create_error_response(f"Processing failed: {str(e)}")
    
    def _validate_input(self, amount: float, currency: str, card_data: Dict[str, str]) -> bool:
        return (amount > 0 and 
                currency in self._supported_currencies and
                'number' in card_data and 
                isinstance(card_data['number'], str))
    
    def _convert_to_base_currency(self, amount: float, currency: str) -> float:
        return ThirdPartyService.convert_currency(amount, currency, 'USD')
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        return {
            'success': False,
            'error': error_msg,
            'transaction_id': None,
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        import datetime
        return datetime.datetime.now().isoformat()

def main():
    legacy_bank = LegacyBankSystem("BANK_001")
    
    payment_processor = PaymentBridge(legacy_bank)
    
    test_payments = [
        (100.50, 'USD', {'number': '4532123456789012', 'cvv': '123'}),
        (85.75, 'EUR', {'number': '5412345678901234', 'cvv': '456'}),
        (-10.0, 'USD', {'number': '4532123456789012', 'cvv': '789'}),
        (50.0, 'GBP', {'number': '123', 'cvv': '000'})
    ]
    
    for amount, currency, card_info in test_payments:
        result = payment_processor.process_payment(amount, currency, card_info)
        print(f"Payment ${amount} {currency}: {'SUCCESS' if result['success'] else 'FAILED'}")
        if result['success']:
            print(f"  Transaction ID: {result['transaction_id']}")
            print(f"  USD Amount: ${result['processed_amount_usd']:.2f}")
        else:
            print(f"  Error: {result['error']}")
        print()

if __name__ == "__main__":
    main()
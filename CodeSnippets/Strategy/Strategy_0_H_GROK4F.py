from abc import ABC, abstractmethod
from typing import Dict, Any

class PaymentError(Exception):
    pass

class PaymentMethod(ABC):
    @abstractmethod
    def handle_payment(self, amount: float, info: Dict[str, Any]) -> str:
        pass

class CreditCardMethod(PaymentMethod):
    def handle_payment(self, amount: float, info: Dict[str, Any]) -> str:
        if 'card_number' not in info:
            raise PaymentError("Card number is required")
        card_num = info['card_number']
        if not isinstance(card_num, str) or len(card_num) < 16:
            raise PaymentError("Invalid card number length")
        if amount <= 0:
            raise PaymentError("Amount must be positive")
        return f"Payment of {amount} successful via credit card ending in {card_num[-4:]}"

class BankTransferMethod(PaymentMethod):
    def handle_payment(self, amount: float, info: Dict[str, Any]) -> str:
        if 'account_number' not in info or 'routing_number' not in info:
            raise PaymentError("Account and routing numbers are required")
        account = info['account_number']
        routing = info['routing_number']
        if not isinstance(account, str) or len(account) != 10:
            raise PaymentError("Invalid account number length")
        if not isinstance(routing, str) or len(routing) != 9:
            raise PaymentError("Invalid routing number length")
        if amount <= 0:
            raise PaymentError("Amount must be positive")
        return f"Payment of {amount} successful via bank transfer to account {account}"

class PaymentMethodFactory:
    def get_method(self, method_type: str) -> PaymentMethod:
        if method_type == 'credit':
            return CreditCardMethod()
        elif method_type == 'bank':
            return BankTransferMethod()
        else:
            raise ValueError(f"Unsupported payment method: {method_type}")

class PaymentService:
    def __init__(self, method: PaymentMethod):
        self._method = method

    def execute_payment(self, amount: float, info: Dict[str, Any]) -> str:
        if amount <= 0:
            raise PaymentError("Amount must be positive")
        return self._method.handle_payment(amount, info)

    def set_method(self, method: PaymentMethod):
        self._method = method

if __name__ == "__main__":
    factory = PaymentMethodFactory()
    service = PaymentService(factory.get_method('credit'))
    
    try:
        result = service.execute_payment(100.0, {'card_number': '1234567890123456'})
        print(result)
    except PaymentError as e:
        print(f"Error: {e}")
    
    try:
        invalid_result = service.execute_payment(100.0, {'card_number': '1234'})
        print(invalid_result)
    except PaymentError as e:
        print(f"Error: {e}")
    
    service.set_method(factory.get_method('bank'))
    
    try:
        bank_result = service.execute_payment(200.0, {
            'account_number': '1234567890',
            'routing_number': '123456789'
        })
        print(bank_result)
    except PaymentError as e:
        print(f"Error: {e}")
    
    try:
        service.execute_payment(-50.0, {'account_number': '1234567890', 'routing_number': '123456789'})
    except PaymentError as e:
        print(f"Error: {e}")
    
    try:
        factory.get_method('invalid')
    except ValueError as e:
        print(f"Error: {e}")
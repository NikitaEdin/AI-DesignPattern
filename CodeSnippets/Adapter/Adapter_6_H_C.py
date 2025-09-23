from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json

class ModernPaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        pass

class LegacyBankSystem:
    def __init__(self, bank_code: str):
        self.bank_code = bank_code
        self._transaction_log = []
    
    def charge_card(self, card_num: str, exp_date: str, cvv: str, amount_cents: int):
        if len(card_num) != 16 or len(cvv) != 3:
            return False, "INVALID_CARD"
        
        transaction_id = f"{self.bank_code}_{len(self._transaction_log) + 1:06d}"
        self._transaction_log.append({
            'id': transaction_id,
            'amount_cents': amount_cents,
            'card_last_four': card_num[-4:]
        })
        
        return True, transaction_id
    
    def get_transaction_status(self, transaction_id: str):
        for txn in self._transaction_log:
            if txn['id'] == transaction_id:
                return "COMPLETED"
        return "NOT_FOUND"

class ThirdPartyService:
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    def submit_charge_request(self, payload: str) -> str:
        try:
            data = json.loads(payload)
            if data.get('amount', 0) <= 0:
                return json.dumps({"status": "error", "message": "Invalid amount"})
            
            return json.dumps({
                "status": "success",
                "reference": f"{self.service_name.upper()}_{hash(payload) % 100000:05d}",
                "fee": data['amount'] * 0.029
            })
        except:
            return json.dumps({"status": "error", "message": "Invalid payload"})

class BankSystemBridge(ModernPaymentGateway):
    def __init__(self, legacy_system: LegacyBankSystem, currency_rates: Optional[Dict[str, float]] = None):
        self._legacy_system = legacy_system
        self._currency_rates = currency_rates or {'USD': 1.0, 'EUR': 0.85, 'GBP': 0.73}
        self._supported_currencies = set(self._currency_rates.keys())
    
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        if currency not in self._supported_currencies:
            return {"success": False, "error": "Unsupported currency"}
        
        if not self._validate_card_data(card_data):
            return {"success": False, "error": "Invalid card data"}
        
        usd_amount = amount / self._currency_rates[currency]
        amount_cents = int(usd_amount * 100)
        
        success, result = self._legacy_system.charge_card(
            card_data['number'],
            card_data['expiry'],
            card_data['cvv'],
            amount_cents
        )
        
        return {
            "success": success,
            "transaction_id": result if success else None,
            "error": result if not success else None,
            "processed_amount": usd_amount if success else None,
            "original_currency": currency
        }
    
    def _validate_card_data(self, card_data: Dict[str, str]) -> bool:
        required_fields = {'number', 'expiry', 'cvv'}
        return all(field in card_data and card_data[field] for field in required_fields)

class ExternalServiceBridge(ModernPaymentGateway):
    def __init__(self, external_service: ThirdPartyService):
        self._external_service = external_service
    
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "card": {
                "number": card_data.get('number', ''),
                "expiry": card_data.get('expiry', ''),
                "cvv": card_data.get('cvv', '')
            }
        })
        
        response_str = self._external_service.submit_charge_request(payload)
        response = json.loads(response_str)
        
        if response.get("status") == "success":
            return {
                "success": True,
                "transaction_id": response["reference"],
                "fee": response.get("fee", 0),
                "processed_amount": amount
            }
        else:
            return {
                "success": False,
                "error": response.get("message", "Unknown error")
            }

class PaymentProcessor:
    def __init__(self):
        self._gateways: List[ModernPaymentGateway] = []
    
    def add_gateway(self, gateway: ModernPaymentGateway):
        self._gateways.append(gateway)
    
    def process_with_fallback(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        for i, gateway in enumerate(self._gateways):
            result = gateway.process_payment(amount, currency, card_data)
            if result["success"]:
                result["gateway_used"] = i
                return result
        
        return {"success": False, "error": "All gateways failed"}

if __name__ == "__main__":
    legacy_bank = LegacyBankSystem("OLDBANK")
    third_party = ThirdPartyService("FastPay")
    
    bank_bridge = BankSystemBridge(legacy_bank)
    service_bridge = ExternalServiceBridge(third_party)
    
    processor = PaymentProcessor()
    processor.add_gateway(bank_bridge)
    processor.add_gateway(service_bridge)
    
    card_info = {
        "number": "1234567890123456",
        "expiry": "12/25",
        "cvv": "123"
    }
    
    result1 = processor.process_with_fallback(100.0, "USD", card_info)
    print(f"Payment 1: {result1}")
    
    result2 = processor.process_with_fallback(50.0, "EUR", card_info)
    print(f"Payment 2: {result2}")
    
    invalid_card = {"number": "123", "expiry": "12/25", "cvv": "12"}
    result3 = processor.process_with_fallback(25.0, "USD", invalid_card)
    print(f"Payment 3: {result3}")
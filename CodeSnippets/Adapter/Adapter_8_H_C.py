from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json

class ModernPaymentInterface(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        pass

class LegacyPaymentSystem:
    def __init__(self, provider_name: str):
        self.provider = provider_name
        self._transactions = {}
    
    def make_payment(self, dollars: float, card_num: str, exp_date: str):
        if dollars <= 0:
            return "FAILED"
        tx_id = f"LEG_{len(self._transactions) + 1:04d}"
        self._transactions[tx_id] = {
            'amount': dollars,
            'card': card_num[-4:],
            'status': 'SUCCESS' if dollars < 10000 else 'PENDING'
        }
        return tx_id
    
    def check_status(self, tx_id: str):
        return self._transactions.get(tx_id, {}).get('status', 'NOT_FOUND')

class CryptoPaymentGateway:
    def __init__(self, wallet_address: str):
        self.wallet = wallet_address
        self._blockchain_txs = {}
    
    def send_crypto(self, amount_btc: float, recipient: str, gas_fee: float = 0.0001):
        if amount_btc <= 0:
            raise ValueError("Invalid amount")
        block_hash = f"0x{hash(f'{amount_btc}{recipient}') % (10**8):08x}"
        self._blockchain_txs[block_hash] = {
            'btc_amount': amount_btc,
            'recipient': recipient,
            'confirmed': amount_btc < 1.0
        }
        return block_hash
    
    def is_confirmed(self, block_hash: str):
        return self._blockchain_txs.get(block_hash, {}).get('confirmed', False)

class LegacyPaymentBridge(ModernPaymentInterface):
    def __init__(self, legacy_system: LegacyPaymentSystem, usd_to_target_rate: float = 1.0):
        self._legacy = legacy_system
        self._rate = usd_to_target_rate
        self._tx_mapping = {}
    
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            usd_amount = amount / self._rate if currency != 'USD' else amount
            card_number = metadata.get('card_number', '4000000000000000')
            exp_date = metadata.get('expiry', '12/25')
            
            legacy_tx_id = self._legacy.make_payment(usd_amount, card_number, exp_date)
            
            modern_tx_id = f"MOD_{len(self._tx_mapping) + 1:06d}"
            self._tx_mapping[modern_tx_id] = legacy_tx_id
            
            return {
                'transaction_id': modern_tx_id,
                'amount': amount,
                'currency': currency,
                'provider': self._legacy.provider,
                'status': 'completed' if legacy_tx_id != 'FAILED' else 'failed'
            }
        except Exception as e:
            return {'transaction_id': None, 'status': 'error', 'message': str(e)}
    
    def get_transaction_status(self, transaction_id: str) -> str:
        legacy_id = self._tx_mapping.get(transaction_id)
        if not legacy_id:
            return 'not_found'
        
        legacy_status = self._legacy.check_status(legacy_id)
        status_map = {'SUCCESS': 'completed', 'PENDING': 'processing', 'FAILED': 'failed'}
        return status_map.get(legacy_status, 'unknown')

class CryptoBridge(ModernPaymentInterface):
    BTC_TO_USD_RATE = 45000.0
    
    def __init__(self, crypto_gateway: CryptoPaymentGateway):
        self._crypto = crypto_gateway
        self._tx_mapping = {}
    
    def process_payment(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            usd_amount = amount if currency == 'USD' else amount * 1.1
            btc_amount = usd_amount / self.BTC_TO_USD_RATE
            recipient = metadata.get('wallet_address', 'default_wallet_123')
            
            block_hash = self._crypto.send_crypto(btc_amount, recipient)
            
            modern_tx_id = f"CRY_{len(self._tx_mapping) + 1:06d}"
            self._tx_mapping[modern_tx_id] = block_hash
            
            return {
                'transaction_id': modern_tx_id,
                'amount': amount,
                'currency': currency,
                'btc_equivalent': btc_amount,
                'block_hash': block_hash,
                'status': 'completed'
            }
        except Exception as e:
            return {'transaction_id': None, 'status': 'error', 'message': str(e)}
    
    def get_transaction_status(self, transaction_id: str) -> str:
        block_hash = self._tx_mapping.get(transaction_id)
        if not block_hash:
            return 'not_found'
        
        return 'completed' if self._crypto.is_confirmed(block_hash) else 'processing'

class UnifiedPaymentProcessor:
    def __init__(self):
        self._processors: List[ModernPaymentInterface] = []
    
    def add_processor(self, processor: ModernPaymentInterface):
        self._processors.append(processor)
    
    def process_with_fallback(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for processor in self._processors:
            result = processor.process_payment(amount, currency, metadata)
            if result.get('status') not in ['error', 'failed']:
                return result
        return None

if __name__ == "__main__":
    legacy_system = LegacyPaymentSystem("OldBank Corp")
    crypto_gateway = CryptoPaymentGateway("wallet_xyz_789")
    
    legacy_bridge = LegacyPaymentBridge(legacy_system, usd_to_target_rate=0.85)
    crypto_bridge = CryptoBridge(crypto_gateway)
    
    unified_processor = UnifiedPaymentProcessor()
    unified_processor.add_processor(legacy_bridge)
    unified_processor.add_processor(crypto_bridge)
    
    payment_data = {
        'card_number': '4532123456789012',
        'expiry': '03/27',
        'wallet_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
    }
    
    result = unified_processor.process_with_fallback(250.0, 'EUR', payment_data)
    print(f"Payment Result: {json.dumps(result, indent=2)}")
    
    if result:
        tx_id = result['transaction_id']
        status = legacy_bridge.get_transaction_status(tx_id)
        print(f"Transaction Status: {status}")
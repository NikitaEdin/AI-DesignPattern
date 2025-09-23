class PaymentStrategy(object):
    def __init__(self, payment_method):
        self.payment_method = payment_method
    
    def process_payment(self, amount):
        if self.payment_method == "credit_card":
            return self._process_credit_card(amount)
        elif self.payment_method == "paypal":
            return self._process_paypal(amount)
    
    def _process_credit_card(self, amount):
        # Process payment using credit card
        pass
    
    def _process_paypal(self, amount):
        # Process payment using PayPal
        pass
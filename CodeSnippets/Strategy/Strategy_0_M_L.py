class PaymentMethod:
    def __init__(self, amount):
        self.amount = amount
        
    def calculate_fee(self):
        return self.amount * 0.1
    
class CashPaymentMethod(PaymentMethod):
    def calculate_fee(self):
        return self.amount * 0.05
    
class CreditCardPaymentMethod(PaymentMethod):
    def calculate_fee(self):
        return self.amount * 0.02

def main():
    payment_methods = [CashPaymentMethod, CreditCardPaymentMethod]
    for method in payment_methods:
        payment = method(100)
        print(f"Total amount with fee: {payment.calculate_fee()}")
        
if __name__ == "__main__":
    main()
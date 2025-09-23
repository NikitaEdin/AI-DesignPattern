class PaymentMethod:
    def process_payment(self, amount):
        raise NotImplementedError("Payment method not implemented")

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount):
        return f"Processed ${amount:.2f} via credit card"

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount):
        return f"Processed ${amount:.2f} via PayPal"

class PaymentCreator:
    @staticmethod
    def create(method_type):
        if method_type.lower() == "credit":
            return CreditCardPayment()
        elif method_type.lower() == "paypal":
            return PayPalPayment()
        else:
            raise ValueError(f"Unsupported payment method: {method_type}")

if __name__ == "__main__":
    try:
        credit_payment = PaymentCreator.create("credit")
        print(credit_payment.process_payment(150.50))

        paypal_payment = PaymentCreator.create("paypal")
        print(paypal_payment.process_payment(75.25))

        invalid_payment = PaymentCreator.create("bitcoin")
    except ValueError as e:
        print(f"Error: {e}")
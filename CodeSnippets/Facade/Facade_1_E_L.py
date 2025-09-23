class User:
    def __init__(self, name):
        self.name = name

class PaymentGateway:
    def __init__(self, user):
        self.user = user

    def make_payment(self, amount):
        print(f"Payment of {amount} made by {self.user.name}")

# Usage example
if __name__ == "__main__":
    user = User("John Doe")
    payment_gateway = PaymentGateway(user)
    payment_gateway.make_payment(100)
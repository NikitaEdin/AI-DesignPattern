class PaymentStrategy(ABC):
    @abstractmethod
    def calculate_payment(self, order: Order) -> float:
        pass


class CreditCardPaymentStrategy(PaymentStrategy):
    def calculate_payment(self, order: Order) -> float:
        return order.get_total() * 1.05


class OnlineBankingPaymentStrategy(PaymentStrategy):
    def calculate_payment(self, order: Order) -> float:
        return order.get_total() * 1.10


class Order:
    def __init__(self, items: List[dict], customer: dict):
        self.items = items
        self.customer = customer

    def get_total(self) -> float:
        total = 0.0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total


def main():
    # Create some orders
    order1 = Order([{"name": "Product 1", "price": 10, "quantity": 2}], {"name": "John Doe"})
    order2 = Order([{"name": "Product 2", "price": 20, "quantity": 1}], {"name": "Jane Doe"})

    # Create payment strategies
    credit_card_strategy = CreditCardPaymentStrategy()
    online_banking_strategy = OnlineBankingPaymentStrategy()

    # Calculate payments for each order using each strategy
    print(f"Order 1: {credit_card_strategy.calculate_payment(order1):.2f}")
    print(f"Order 2: {online_banking_strategy.calculate_payment(order2):.2f}")


if __name__ == "__main__":
    main()
# Classes and Interfaces for Facade Pattern
class PaymentGateway:
    def make_payment(self, amount):
        print("Payment of $", amount, "made through payment gateway.")

class DeliveryService:
    def ship_order(self, order):
        print("Order", order, "shipped through delivery service.")

# Facade Class
class OrderProcessingSystem:
    def __init__(self, payment_gateway, delivery_service):
        self.payment_gateway = payment_gateway
        self.delivery_service = delivery_service

    def process_order(self, order):
        self.payment_gateway.make_payment(order.total)
        self.delivery_service.ship_order(order)
        print("Order", order, "processed successfully.")

# Usage Example
if __name__ == "__main__":
    payment_gateway = PaymentGateway()
    delivery_service = DeliveryService()
    order_processing_system = OrderProcessingSystem(payment_gateway, delivery_service)
    order = {"total": 100.0}
    order_processing_system.process_order(order)
# Order class
class Order:
    def __init__(self, customer):
        self.customer = customer
        self.state = OrderCreatedState(self)
    
    def change_state(self, new_state):
        self.state = new_state
        return self.state
    
# Order State class
class OrderState:
    def __init__(self, order):
        self.order = order
    
    def process(self):
        raise NotImplementedError
        
# Payment Due state class
class PaymentDueState(OrderState):
    def process(self):
        if self.order.customer.balance >= self.order.total_price:
            self.order.state = ProcessingState(self.order)
            return "Processing"
        else:
            self.order.state = CancelledState(self.order)
            return "Cancelled"
    
# Payment Processed state class
class ProcessingState(OrderState):
    def process(self):
        if self.order.customer.balance < self.order.total_price:
            self.order.state = CancelledState(self.order)
            return "Cancelled"
        else:
            self.order.state = DeliveredState(self.order)
            return "Delivered"
    
# Payment Cancelled state class
class CancelledState(OrderState):
    def process(self):
        self.order.state = OrderCreatedState(self.order)
        return "Cancelled"
    
# Payment Delivered state class
class DeliveredState(OrderState):
    def process(self):
        self.order.state = OrderCompletedState(self.order)
        return "Delivered"
    
# Order Completed state class
class OrderCompletedState(OrderState):
    def process(self):
        return "Completed"
        
# Customer class
class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    
# Main section
if __name__ == "__main__":
    # Create a customer and an order
    customer = Customer("John Doe", 1000)
    order = Order(customer)
    
    # Change the state of the order to payment due
    order.change_state(PaymentDueState(order))
    
    # Process the order
    print(order.process())
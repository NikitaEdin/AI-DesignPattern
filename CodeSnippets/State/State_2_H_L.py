# State Design Pattern Example in Python
class OrderState:
    def __init__(self, order):
        self.order = order
    
    def process(self):
        pass

class NewState(OrderState):
    def process(self):
        print("New state")

class PendingState(OrderState):
    def process(self):
        print("Pending state")

class ProcessingState(OrderState):
    def process(self):
        print("Processing state")

class CompletedState(OrderState):
    def process(self):
        print("Completed state")

# Usage Example
order = Order()
order.setState(NewState(order))
order.process() # Output: New state
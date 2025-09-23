class OrderCommand:
    def __init__(self, order_id):
        self.order_id = order_id

    def execute(self):
        # Execute the command and return a result
        print(f"Executing OrderCommand with ID {self.order_id}")
        return f"Order {self.order_id} executed"
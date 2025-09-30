class Inventory:
    def check(self, item):
        return f"{item} available"

class Payment:
    def process(self, amount):
        return f"Payment of {amount} processed"

class Delivery:
    def schedule(self, item):
        return f"Delivery scheduled for {item}"

class OrderSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.delivery = Delivery()
    
    def order(self, item, amount):
        try:
            print("Placing order...")
            print(self.inventory.check(item))
            print(self.payment.process(amount))
            print(self.delivery.schedule(item))
            return "Order successful"
        except Exception as e:
            return f"Order failed: {e}"

if __name__ == "__main__":
    system = OrderSystem()
    result = system.order("laptop", 1200)
    print(result)
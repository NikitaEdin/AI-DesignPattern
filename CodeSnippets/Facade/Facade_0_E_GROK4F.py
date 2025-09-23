class Inventory:
    def checkStock(self, item):
        print(f"Checking stock for {item}")
        return True

    def deduct(self, item):
        print(f"Deducting {item} from stock")

class Payment:
    def process(self, amount):
        print(f"Processing payment of ${amount}")
        return True

class Shipping:
    def ship(self, item):
        print(f"Shipping {item}")

class OrderProcessor:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()

    def placeOrder(self, item, amount):
        if self.inventory.checkStock(item):
            self.inventory.deduct(item)
            self.payment.process(amount)
            self.shipping.ship(item)
            print("Order placed successfully")

if __name__ == "__main__":
    processor = OrderProcessor()
    processor.placeOrder("laptop", 1000)
class Inventory:
    def check_stock(self, item):
        stock = {"laptop": 5, "phone": 3}
        return stock.get(item, 0) > 0

class Payment:
    def process_payment(self, card, amount):
        return len(card) == 16 and amount > 0

class Shipping:
    def dispatch(self, address):
        return address.strip() != ""

class ShopService:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()

    def buy(self, item, amount, card, address):
        if not self.inventory.check_stock(item):
            raise ValueError("Out of stock")
        if not self.payment.process_payment(card, amount):
            raise ValueError("Payment failed")
        if not self.shipping.dispatch(address):
            address = "Unknown"
        return {"item": item, "success": True}

if __name__ == "__main__":
    shop = ShopService()
    order = shop.buy("laptop", 999, "1234567890123456", "42 Galaxy Way")
    print(order)
class Order:
    def __init__(self, customer_name, item):
        self.customer_name = customer_name
        self.item = item

    def execute(self):
        print(f"Order placed by {self.customer_name} for {self.item}")

class Delivery:
    def __init__(self, order):
        self.order = order

    def execute(self):
        print("Delivery started")
        self.order.execute()
        print("Delivery completed")

def main():
    order = Order("John Doe", "Macbook Pro")
    delivery = Delivery(order)
    delivery.execute()

if __name__ == "__main__":
    main()
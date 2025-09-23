# Factory pattern implementation

class Product:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(f"Name: {self.name}")


class CarFactory:
    @staticmethod
    def create_product(name):
        return Product(name)


if __name__ == "__main__":
    # Create a product using the factory method
    product = CarFactory.create_product("Ford")

    # Use the created product
    product.print_name()
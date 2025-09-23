class Product:
    """
    Abstract product class that represents a product of a factory.
    """
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def use(self):
        print("Using " + self.get_name())

class ConcreteProductA(Product):
    """
    Concrete product class that represents a specific product of the factory.
    """
    def __init__(self, name):
        super().__init__(name)
    
    def use(self):
        print("Using " + self.get_name() + " with option A")

class ConcreteProductB(Product):
    """
    Concrete product class that represents a specific product of the factory.
    """
    def __init__(self, name):
        super().__init__(name)
    
    def use(self):
        print("Using " + self.get_name() + " with option B")

class Factory:
    """
    Abstract factory class that creates concrete products of the factory.
    """
    @staticmethod
    def create_product(option):
        if option == 'A':
            return ConcreteProductA('Product A')
        elif option == 'B':
            return ConcreteProductB('Product B')
        else:
            raise Exception("Invalid option")
    
def main():
    """
    Main function that demonstrates the usage of the factory.
    """
    product = Factory.create_product('A')
    product.use()
    print("\n\n")
    product = Factory.create_product('B')
    product.use()

if __name__ == "__main__":
    main()
import abc

class Product(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def operation(self):
        pass

class ConcreteProduct1(Product):
    def operation(self):
        print("ConcreteProduct1")

class ConcreteProduct2(Product):
    def operation(self):
        print("ConcreteProduct2")

class Creator:
    @staticmethod
    def create_product():
        return ConcreteProduct1()

# Usage example
if __name__ == "__main__":
    creator = Creator()
    product1 = creator.create_product()
    product1.operation()  # Output: ConcreteProduct1
from abc import ABC, abstractmethod
from typing import Dict, Type, Any

class Product(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class ConcreteProductA(Product):
    def render(self) -> str:
        return "ProductA instance"

class ConcreteProductB(Product):
    def render(self) -> str:
        return "ProductB instance"

class Creator(ABC):
    @abstractmethod
    def create_product(self, product_type: str, **kwargs) -> Product:
        pass

class ConcreteCreator(Creator):
    def __init__(self):
        self._registry: Dict[str, Type[Product]] = {
            'A': ConcreteProductA,
            'B': ConcreteProductB
        }
    
    def register_product(self, product_type: str, product_class: Type[Product]):
        self._registry[product_type] = product_class
    
    def create_product(self, product_type: str, **kwargs) -> Product:
        if product_type not in self._registry:
            raise ValueError(f"Unknown product type: {product_type}")
        return self._registry[product_type](**kwargs)

class Client:
    def __init__(self, creator: Creator):
        self._creator = creator
    
    def process(self, product_type: str) -> str:
        product = self._creator.create_product(product_type)
        return product.render()

if __name__ == "__main__":
    creator = ConcreteCreator()
    client = Client(creator)
    
    result_a = client.process('A')
    result_b = client.process('B')
    
    print(result_a)
    print(result_b)
from abc import ABC, abstractmethod

class ConstructorInterface(ABC):
    @abstractmethod
    def add_engine(self):
        pass
    
    @abstractmethod
    def add_wheels(self):
        pass
    
    @abstractmethod
    def build(self):
        pass

class Product:
    def __init__(self):
        self.parts = []
    
    def add_part(self, part):
        self.parts.append(part)

class ConcreteConstructor(ConstructorInterface):
    def __init__(self):
        self.product = Product()
    
    def add_engine(self):
        self.product.add_part("Engine")
        return self
    
    def add_wheels(self):
        self.product.add_part("Wheels")
        return self
    
    def build(self):
        return self.product

if __name__ == "__main__":
    constructor = ConcreteConstructor()
    car = constructor.add_engine().add_wheels().build()
    print(car.parts)
from abc import ABC, abstractmethod
class Product(ABC):
    @abstractmethod
    def use(self) -> str: pass
class RedProduct(Product):
    def use(self) -> str:
        return "Using red product"
class BlueProduct(Product):
    def use(self) -> str:
        return "Using blue product"
class Creator:
    def make(self, kind: str) -> Product:
        if kind == "red": return RedProduct()
        if kind == "blue": return BlueProduct()
        raise ValueError("Unknown kind")
if __name__ == "__main__":
    maker = Creator()
    for name in ("red","blue"):
        print(maker.make(name).use())
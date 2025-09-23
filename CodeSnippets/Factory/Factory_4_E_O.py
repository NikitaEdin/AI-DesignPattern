class Product:
    def operate(self) -> str:
        raise NotImplementedError

class Car(Product):
    def operate(self) -> str:
        return "Car driving"

class Bike(Product):
    def operate(self) -> str:
        return "Bike pedaling"

class Creator:
    def create(self, kind: str) -> Product:
        if kind == "car":
            return Car()
        if kind == "bike":
            return Bike()
        raise ValueError("Unknown product")

if __name__ == "__main__":
    creator = Creator()
    for kind in ("car", "bike"):
        product = creator.create(kind)
        print(product.operate())
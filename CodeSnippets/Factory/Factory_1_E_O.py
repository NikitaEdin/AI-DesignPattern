class Product:
    def operation(self):
        raise NotImplementedError

class Apple(Product):
    def __init__(self, color):
        self.color = color
    def operation(self):
        return f"Apple of color {self.color}"

class Banana(Product):
    def __init__(self, length):
        self.length = length
    def operation(self):
        return f"Banana of length {self.length}cm"

class Creator:
    def create(self, kind, **kwargs):
        if kind == "apple":
            return Apple(kwargs.get("color", "red"))
        if kind == "banana":
            return Banana(kwargs.get("length", 10))
        raise ValueError("Unknown kind")

if __name__ == "__main__":
    maker = Creator()
    a = maker.create("apple", color="green")
    b = maker.create("banana", length=15)
    print(a.operation())
    print(b.operation())
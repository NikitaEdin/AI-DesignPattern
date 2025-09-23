class Product:
    def __init__(self):
        self.parts = []
    
    def add_part(self, part):
        self.parts.append(part)
    
    def show(self):
        return f"Product parts: {', '.join(self.parts)}"

class Creator:
    def __init__(self):
        self.product = Product()
    
    def add_engine(self, engine):
        self.product.add_part(f"Engine: {engine}")
        return self
    
    def add_wheels(self, wheels):
        self.product.add_part(f"Wheels: {wheels}")
        return self
    
    def build(self):
        return self.product

if __name__ == "__main__":
    car = Creator().add_engine("V8").add_wheels("4").build()
    print(car.show())
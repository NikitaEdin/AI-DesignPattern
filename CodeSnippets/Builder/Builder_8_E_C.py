class Product:
    def __init__(self):
        self.parts = []
    
    def add_part(self, part):
        self.parts.append(part)
    
    def show_parts(self):
        return f"Product parts: {', '.join(self.parts)}"

class CarAssembler:
    def __init__(self):
        self.product = Product()
    
    def add_engine(self, engine_type):
        self.product.add_part(f"Engine: {engine_type}")
        return self
    
    def add_wheels(self, count):
        self.product.add_part(f"Wheels: {count}")
        return self
    
    def add_body(self, body_type):
        self.product.add_part(f"Body: {body_type}")
        return self
    
    def get_product(self):
        return self.product

if __name__ == "__main__":
    assembler = CarAssembler()
    car = assembler.add_engine("V6").add_wheels(4).add_body("Sedan").get_product()
    print(car.show_parts())
class Director:
    def __init__(self):
        self.builder = None
    
    def construct(self, builder):
        self.builder = builder
        return self.builder
    
    def build_minimal_viable_product(self):
        self.builder.build_body()
        self.builder.build_head()
        self.builder.build_wheels()
        return self.builder.get_result()

class CarBuilder:
    def __init__(self, director):
        self.director = director
    
    def build_body(self):
        print("Building body of the car")
    
    def build_head(self):
        print("Building head of the car")
    
    def build_wheels(self):
        print("Building wheels of the car")
    
    def get_result(self):
        return "Car"

if __name__ == "__main__":
    director = Director()
    builder = CarBuilder(director)
    car = director.construct(builder).build_minimal_viable_product()
    print(car)
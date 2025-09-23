class CarBuilder:
    def __init__(self):
        self.car = None
    
    def set_make(self, make):
        self.car = {'make': make}
        return self
    
    def set_model(self, model):
        self.car['model'] = model
        return self
    
    def set_year(self, year):
        self.car['year'] = year
        return self
    
    def build(self):
        return self.car
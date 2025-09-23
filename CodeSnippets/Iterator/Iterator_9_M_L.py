class ProductIterator:
    def __init__(self, products):
        self.products = products
        self.index = 0
    
    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
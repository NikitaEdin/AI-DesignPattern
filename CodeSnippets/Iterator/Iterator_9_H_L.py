class ProductIterator(object):
    def __init__(self, products):
        self.products = products
        self.index = 0

    def next(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration

class ProductDatabase(object):
    def __init__(self, products=[]):
        self.products = products

    def __iter__(self):
        return ProductIterator(self.products)

def main():
    db = ProductDatabase(['Apple', 'Orange', 'Grapes'])
    for product in db:
        print(product)
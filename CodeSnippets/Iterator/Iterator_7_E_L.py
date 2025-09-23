class ProductsIterator:
    def __init__(self, products):
        self.products = products
        self.index = 0

    def has_next(self):
        return self.index < len(self.products)

    def next(self):
        if self.has_next():
            item = self.products[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration()

class ProductsCollection:
    def __init__(self, products):
        self.products = products

    def iterator(self):
        return ProductsIterator(self.products)

if __name__ == "__main__":
    products = ["apple", "banana", "cherry"]
    collection = ProductsCollection(products)

    for product in collection.iterator():
        print(product)
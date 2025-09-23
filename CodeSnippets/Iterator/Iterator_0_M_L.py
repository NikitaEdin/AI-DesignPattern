class ProductDatabase:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        self._products.append(product)

    def get_iterator(self):
        return ProductIterator(self._products)

class ProductIterator:
    def __init__(self, products):
        self._products = products
        self._index = 0

    def has_next(self):
        return self._index < len(self._products)

    def next(self):
        if not self.has_next():
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product

# Example usage:
if __name__ == "__main__":
    database = ProductDatabase()
    database.add_product("Product A")
    database.add_product("Product B")
    database.add_product("Product C")

    iterator = database.get_iterator()
    for product in iterator:
        print(product)
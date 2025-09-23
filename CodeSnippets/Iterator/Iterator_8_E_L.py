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

class Products:
    def __init__(self, products):
        self.products = products

    def iterator(self):
        return ProductIterator(self.products)

def main():
    products = [("apple", 10), ("banana", 20), ("orange", 30)]
    product_list = Products(products)
    for product in product_list.iterator():
        print(product[0], product[1])

if __name__ == "__main__":
    main()
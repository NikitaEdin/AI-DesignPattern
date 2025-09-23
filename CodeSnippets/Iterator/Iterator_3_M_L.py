[PYTHON]
class ProductIterator:
    def __init__(self, products):
        self.products = products
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.products)
    
    def next(self):
        if not self.has_next():
            raise StopIteration
        product = self.products[self.index]
        self.index += 1
        return product

class ProductDatabase:
    def __init__(self, products):
        self.products = products
    
    def get_iterator(self):
        return ProductIterator(self.products)

products = ["Apple", "Orange", "Grapes"]
database = ProductDatabase(products)

for product in database.get_iterator():
    print(product)
```
[/PYTHON]
The code above implements the Iterator design pattern using a class named `ProductIterator` that keeps track of an index and iterates through a list of products, and a class named `ProductDatabase` that provides an iterator to iterate through its product list. The `main` section demonstrates usage by creating a database with some products and iterating through them using the `get_iterator` method.

Note that this is just one way to implement the Iterator pattern in Python, and there are many other ways to do it. The key idea is to provide a way for clients to iterate through a collection of objects without having to know its internal implementation details.
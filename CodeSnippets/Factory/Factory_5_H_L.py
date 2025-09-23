class ProductA:
    def __init__(self):
        pass

class ProductB:
    def __init__(self):
        pass

class Factory:
    @staticmethod
    def create(name):
        if name == 'ProductA':
            return ProductA()
        elif name == 'ProductB':
            return ProductB()
        else:
            raise ValueError('Invalid product')

def main():
    factory = Factory()
    product_a = factory.create('ProductA')
    product_b = factory.create('ProductB')

if __name__ == '__main__':
    main()
class MyCollection:
    def __init__(self):
        self.data = [1, 2, 3, 4, 5]

    def create_forward(self):
        return self._MyOrder(self)

    class _MyOrder:
        def __init__(self, collection):
            self.collection = collection
            self.pos = 0

        def has_next(self):
            return self.pos < len(self.collection.data)

        def get_next(self):
            item = self.collection.data[self.pos]
            self.pos += 1
            return item


if __name__ == "__main__":
    c = MyCollection()
    o = c.create_forward()
    while o.has_next():
        print(o.get_next(), end=" ")
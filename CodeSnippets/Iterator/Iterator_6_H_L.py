class IteratorExample:
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.items)
    
    def next(self):
        if not self.has_next():
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item

if __name__ == "__main__":
    items = [1, 2, 3, 4, 5]
    iterator = IteratorExample(items)
    
    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break
class ItemIterator:
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def next(self):
        if self.hasNext():
            item = self.items[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration()
    
    def hasNext(self):
        return self.index < len(self.items)
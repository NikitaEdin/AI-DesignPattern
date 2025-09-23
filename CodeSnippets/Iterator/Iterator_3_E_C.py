class NumberCollection:
    def __init__(self, numbers):
        self._numbers = numbers
    
    def create_traverser(self):
        return NumberTraverser(self._numbers)

class NumberTraverser:
    def __init__(self, numbers):
        self._numbers = numbers
        self._position = 0
    
    def has_next(self):
        return self._position < len(self._numbers)
    
    def next(self):
        if not self.has_next():
            raise StopIteration()
        value = self._numbers[self._position]
        self._position += 1
        return value

if __name__ == "__main__":
    collection = NumberCollection([1, 2, 3, 4, 5])
    traverser = collection.create_traverser()
    
    while traverser.has_next():
        print(traverser.next())
class NumberCollection:
    def __init__(self, numbers):
        self.numbers = numbers
    
    def create_traverser(self):
        return NumberTraverser(self.numbers)

class NumberTraverser:
    def __init__(self, numbers):
        self.numbers = numbers
        self.position = 0
    
    def has_next(self):
        return self.position < len(self.numbers)
    
    def next(self):
        if self.has_next():
            value = self.numbers[self.position]
            self.position += 1
            return value
        raise StopIteration

if __name__ == "__main__":
    collection = NumberCollection([1, 2, 3, 4, 5])
    traverser = collection.create_traverser()
    
    while traverser.has_next():
        print(traverser.next())
class NumberSequence:
    def __init__(self, max_value):
        self.max_value = max_value
    
    def create_traverser(self):
        return SequenceTraverser(self)

class SequenceTraverser:
    def __init__(self, sequence):
        self.sequence = sequence
        self.current = 0
    
    def has_next(self):
        return self.current < self.sequence.max_value
    
    def next(self):
        if self.has_next():
            value = self.current
            self.current += 1
            return value
        raise StopIteration

if __name__ == "__main__":
    numbers = NumberSequence(5)
    traverser = numbers.create_traverser()
    
    while traverser.has_next():
        print(traverser.next())
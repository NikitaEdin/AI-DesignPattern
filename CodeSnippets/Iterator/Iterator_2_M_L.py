class MyIterator:
    def __init__(self, iterable):
        self.items = iterable
        self.index = 0

    def __next__(self):
        if self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration

def my_function():
    # Create an iterator over a list of numbers
    numbers = [1, 2, 3, 4, 5]
    iterator = MyIterator(numbers)

    # Use the iterator in a loop
    for item in iterator:
        print(item)

if __name__ == "__main__":
    my_function()
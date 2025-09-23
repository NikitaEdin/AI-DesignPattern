# A simple example of a Python Iterator
class Iterable:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)

class MyIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.index = 0

    def __next__(self):
        if self.index >= len(self.iterable.items):
            raise StopIteration
        item = self.iterable.items[self.index]
        self.index += 1
        return item

def main():
    iterable = Iterable([1, 2, 3])
    iterator = MyIterator(iterable)
    for item in iterator:
        print(item)

if __name__ == "__main__":
    main()
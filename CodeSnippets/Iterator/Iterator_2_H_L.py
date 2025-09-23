# MyContainer class
class MyContainer:
    def __init__(self, items):
        self._items = items

    # Define an iterator for iterating over the container's elements
    def __iter__(self):
        return MyIterator(self._items)

# MyIterator class
class MyIterator:
    def __init__(self, items):
        self._items = items
        self._index = 0

    # Implement the hasNext() method to check if there are more elements to iterate over
    def hasNext(self):
        return self._index < len(self._items)

    # Implement the next() method to retrieve the next element in the iteration
    def next(self):
        if not self.hasNext():
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item

# Usage example
if __name__ == "__main__":
    # Create a container with some items
    container = MyContainer(["apple", "banana", "cherry"])

    # Use the iterator to iterate over the elements
    for item in container:
        print(item)
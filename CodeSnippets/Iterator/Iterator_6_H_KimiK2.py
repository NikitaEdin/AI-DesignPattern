class SequentialStream:
    def __init__(self, data):
        self._data = data
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position >= len(self._data):
            raise StopIteration
        value = self._data[self._position]
        self._position += 1
        return value

class ReverseStream:
    def __init__(self, data):
        self._data = data
        self._position = len(data) - 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position < 0:
            raise StopIteration
        value = self._data[self._position]
        self._position -= 1
        return value

class SkippingStream:
    def __init__(self, data, skip):
        self._data = data
        self._skip = skip
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration
        value = self._data[self._index]
        self._index += self._skip
        return value

class DataCollection:
    def __init__(self):
        self._items = []
    
    def add_item(self, item):
        self._items.append(item)
    
    def get_items(self):
        return SequentialStream(self._items)
    
    def get_reverse_items(self):
        return ReverseStream(self._items)
    
    def get_skipping_items(self, skip):
        return SkippingStream(self._items, skip)

def main():
    collection = DataCollection()
    for i in range(10):
        collection.add_item(i)
    
    print("Sequential:")
    for item in collection.get_items():
        print(item, end=" ")
    print()
    
    print("Reverse:")
    for item in collection.get_reverse_items():
        print(item, end=" ")
    print()
    
    print("Skip 2:")
    for item in collection.get_skipping_items(2):
        print(item, end=" ")
    print()

if __name__ == "__main__":
    main()
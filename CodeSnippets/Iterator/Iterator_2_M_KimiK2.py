class BookCollection:
    def __init__(self):
        self._items = []
    
    def add(self, book):
        self._items.append(book)
    
    def __iter__(self):
        return BookCollectionNavigator(self._items)
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]

class BookCollectionNavigator:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._collection):
            item = self._collection[self._index]
            self._index += 1
            return item
        raise StopIteration
    
    def is_done(self):
        return self._index >= len(self._collection)

if __name__ == "__main__":
    books = BookCollection()
    books.add("1984")
    books.add("Brave New World")
    books.add("Fahrenheit 451")
    
    for book in books:
        print(book)
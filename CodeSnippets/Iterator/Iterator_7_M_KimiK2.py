class BookCollection:
    def __init__(self):
        self._books = []

    def add_book(self, title):
        self._books.append(title)

    def __len__(self):
        return len(self._books)

    def __getitem__(self, index):
        if index >= len(self._books):
            raise IndexError("Index out of range")
        return self._books[index]

    def __iter__(self):
        return BookCollectionSequence(self)

class BookCollectionSequence:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0

    def __next__(self):
        try:
            item = self._collection[self._index]
            self._index += 1
            return item
        except IndexError:
            raise StopIteration from None

    def __iter__(self):
        return self

if __name__ == "__main__":
    shelf = BookCollection()
    shelf.add_book("1984")
    shelf.add_book("Brave New World")
    shelf.add_book("Fahrenheit 451")

    for book in shelf:
        print(book)
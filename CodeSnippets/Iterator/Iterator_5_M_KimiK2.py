class BookShelf:
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def create_browse_order(self):
        return BookBrowseOrder(self)

    @property
    def items(self):
        return self._books


class BookBrowseOrder:
    def __init__(self, shelf):
        self._shelf = shelf
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._shelf.items):
            book = self._shelf.items[self._index]
            self._index += 1
            return book
        raise StopIteration


if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("1984")
    shelf.add_book("Brave New World")
    shelf.add_book("Fahrenheit 451")

    for book in shelf.create_browse_order():
        print(book)
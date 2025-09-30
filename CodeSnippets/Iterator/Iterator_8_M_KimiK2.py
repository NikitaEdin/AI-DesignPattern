class BookShelf:
    def __init__(self):
        self.books = []
    def add_book(self, title):
        self.books.append(title)
    def create_books_view(self):
        return BookView(self)


class BookView:
    def __init__(self, shelf):
        self._shelf = shelf
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._shelf.books):
            raise StopIteration
        current = self._shelf.books[self._index]
        self._index += 1
        return current


if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("1984")
    shelf.add_book("Brave New World")
    shelf.add_book("Fahrenheit 451")
    view = shelf.create_books_view()
    for book in view:
        print(book)
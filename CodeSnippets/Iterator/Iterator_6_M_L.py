class BookShelfIterator:
    def __init__(self, book_shelf):
        self.book_shelf = book_shelf
        self.current_index = 0

    def has_next(self):
        return self.current_index < len(self.book_shelf)

    def next(self):
        if not self.has_next():
            raise StopIteration
        book = self.book_shelf[self.current_index]
        self.current_index += 1
        return book

class BookShelf:
    def __init__(self, books=[]):
        self.books = books

    def __iter__(self):
        return BookShelfIterator(self)

    def add_book(self, book):
        self.books.append(book)

if __name__ == "__main__":
    book_shelf = BookShelf()
    for i in range(5):
        book_shelf.add_book("Book {}".format(i))

    iterator = iter(book_shelf)
    while True:
        try:
            book = next(iterator)
            print(book)
        except StopIteration:
            break
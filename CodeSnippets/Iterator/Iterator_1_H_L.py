class BookShelfIterator:
    def __init__(self, book_shelf):
        self.book_shelf = book_shelf
        self.current_index = 0

    def has_next(self):
        return self.current_index < len(self.book_shelf.books)

    def next(self):
        if not self.has_next():
            raise StopIteration
        book = self.book_shelf.books[self.current_index]
        self.current_index += 1
        return book

class BookShelf:
    def __init__(self, books):
        self.books = books

    def __iter__(self):
        return BookShelfIterator(self)

if __name__ == "__main__":
    book_shelf = BookShelf(["Harry Potter", "The Dark Tower", "The Lord of the Rings"])
    for book in book_shelf:
        print(book)
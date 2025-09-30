class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_reader(self):
        return BookReader(self)


class BookReader:
    def __init__(self, shelf):
        self.shelf = shelf
        self.index = 0

    def has_next(self):
        return self.index < len(self.shelf.books)

    def next(self):
        book = self.shelf.books[self.index]
        self.index += 1
        return book


if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Book A")
    shelf.add_book("Book B")
    reader = shelf.create_reader()
    while reader.has_next():
        print(reader.next())
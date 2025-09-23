class BookTraverser:
    def __init__(self, books):
        self.books = books
        self.position = 0

    def __next__(self):
        if self.position >= len(self.books):
            raise StopIteration
        book = self.books[self.position]
        self.position += 1
        return book

class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __iter__(self):
        return BookTraverser(self.books)

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Book One")
    shelf.add_book("Book Two")
    shelf.add_book("Book Three")
    for book in shelf:
        print(book)
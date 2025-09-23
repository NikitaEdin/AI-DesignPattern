class Book:
    def __init__(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        self.title = title

class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if not isinstance(book, Book):
            raise ValueError("Only Book instances can be added")
        self.books.append(book)

    def __iter__(self):
        return BookViewer(self)

class BookViewer:
    def __init__(self, shelf):
        self.shelf = shelf
        self.current = 0

    def __next__(self):
        if self.current >= len(self.shelf.books):
            raise StopIteration
        book = self.shelf.books[self.current]
        self.current += 1
        return book

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("Python Basics"))
    shelf.add_book(Book("Design Patterns"))
    shelf.add_book(Book("Advanced Algorithms"))
    for book in shelf:
        print(book.title)
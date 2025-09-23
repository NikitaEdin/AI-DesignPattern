class Book:
    def __init__(self, title):
        self.title = title

class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
        else:
            raise ValueError("Must add Book instances only")

    def create_selector(self):
        return BookSelector(self)

class BookSelector:
    def __init__(self, shelf):
        self.shelf = shelf
        self.position = 0

    def has_next(self):
        return self.position < len(self.shelf.books)

    def next(self):
        if self.has_next():
            book = self.shelf.books[self.position]
            self.position += 1
            return book
        else:
            raise StopIteration("No more books available")

    def reset(self):
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("Python Basics"))
    shelf.add_book(Book("Design Patterns"))
    shelf.add_book(Book("Advanced Coding"))

    selector = shelf.create_selector()
    print("First traversal:")
    for book in selector:
        print(book.title)

    selector.reset()
    print("\nAfter reset:")
    while selector.has_next():
        print(selector.next().title)
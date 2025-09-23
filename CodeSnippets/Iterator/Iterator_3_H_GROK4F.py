class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_traverser(self):
        return BookTraverser(self.books[:])

class BookTraverser:
    def __init__(self, books):
        self.books = books
        self.current_index = 0

    def current_book(self):
        if self.books and 0 <= self.current_index < len(self.books):
            return self.books[self.current_index]
        return None

    def has_next(self):
        return bool(self.books) and self.current_index < len(self.books) - 1

    def next_book(self):
        if not self.has_next():
            return None
        self.current_index += 1
        return self.current_book()

    def has_previous(self):
        return bool(self.books) and self.current_index > 0

    def previous_book(self):
        if not self.has_previous():
            return None
        self.current_index -= 1
        return self.current_book()

    def reset(self):
        self.current_index = 0

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("1984", "George Orwell"))
    shelf.add_book(Book("Brave New World", "Aldous Huxley"))
    shelf.add_book(Book("Fahrenheit 451", "Ray Bradbury"))

    traverser = shelf.create_traverser()

    print("Forward traversal:")
    book = traverser.current_book()
    while book:
        print(f"{book.title} by {book.author}")
        book = traverser.next_book()

    print("\nBackward traversal from end:")
    book = traverser.current_book()
    while book:
        print(f"{book.title} by {book.author}")
        book = traverser.previous_book()

    print("\nAfter reset, first book:")
    traverser.reset()
    book = traverser.current_book()
    if book:
        print(f"{book.title} by {book.author}")

    shelf.add_book(Book("Added After", "Unknown"))
    print("\nSnapshot does not include added book; current book still:")
    print(f"{traverser.current_book().title} by {traverser.current_book().author}")

    empty_shelf = BookShelf()
    empty_traverser = empty_shelf.create_traverser()
    print("\nEmpty collection current book:", empty_traverser.current_book())
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_forward_walker(self):
        return ForwardWalker(self.books)

    def create_reverse_walker(self):
        return ReverseWalker(self.books)

class ForwardWalker:
    def __init__(self, books):
        self.books = books
        self.current_index = 0

    def has_next(self):
        return self.current_index < len(self.books)

    def next(self):
        if not self.has_next():
            raise StopIteration
        book = self.books[self.current_index]
        self.current_index += 1
        return book

    def reset(self):
        self.current_index = 0

class ReverseWalker:
    def __init__(self, books):
        self.books = books
        self.current_index = len(books) - 1 if books else -1

    def has_next(self):
        return self.current_index >= 0

    def next(self):
        if not self.has_next():
            raise StopIteration
        book = self.books[self.current_index]
        self.current_index -= 1
        return book

    def reset(self):
        self.current_index = len(self.books) - 1 if self.books else -1

if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("1984", "George Orwell"))
    lib.add_book(Book("To Kill a Mockingbird", "Harper Lee"))
    lib.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald"))

    print("Forward traversal:")
    walker = lib.create_forward_walker()
    while walker.has_next():
        print(walker.next())

    print("\nReverse traversal:")
    walker = lib.create_reverse_walker()
    while walker.has_next():
        print(walker.next())

    print("\nReset and forward again:")
    walker.reset()
    while walker.has_next():
        print(walker.next())

    print("\nEmpty library:")
    empty_lib = Library()
    empty_walker = empty_lib.create_forward_walker()
    if not empty_walker.has_next():
        print("No books available.")
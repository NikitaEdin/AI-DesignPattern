class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self._valid = True

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value

    def __str__(self):
        return f"{self.title} by {self.author}"


class Library:
    def __init__(self):
        self._books = []
        self._mod_count = 0

    def add_book(self, book):
        self._books.append(book)
        self._mod_count += 1

    def remove_book(self, book):
        if book in self._books:
            self._books.remove(book)
            self._mod_count += 1

    def __iter__(self):
        return BookTraverser(self)

    def create_traverser(self):
        return BookTraverser(self)


class BookTraverser:
    def __init__(self, library):
        self._library = library
        self._mod_count = library._mod_count
        self._index = 0

    def __next__(self):
        while self._index < len(self._library._books):
            if self._library._mod_count != self._mod_count:
                raise RuntimeError("Library modified during traversal")
            book = self._library._books[self._index]
            self._index += 1
            if book.valid:
                return book
        raise StopIteration

    def next(self):
        return self.__next__()

    def has_next(self):
        if self._library._mod_count != self._mod_count:
            raise RuntimeError("Library modified during traversal")
        return self._index < len(self._library._books)


if __name__ == "__main__":
    lib = Library()
    book1 = Book("1984", "George Orwell")
    book2 = Book("Brave New World", "Aldous Huxley")
    invalid_book = Book("Invalid Book", "Unknown")
    book3 = Book("Fahrenheit 451", "Ray Bradbury")

    lib.add_book(book1)
    lib.add_book(book2)
    lib.add_book(invalid_book)
    lib.add_book(book3)

    invalid_book.valid = False

    print("Using for loop (skips invalid):")
    for book in lib:
        print(book)

    print("\nManual traversal with modification:")
    trav = lib.create_traverser()
    print(trav.next())  # 1984

    lib.add_book(Book("Animal Farm", "George Orwell"))

    try:
        print(trav.next())  # Should raise error
    except RuntimeError as e:
        print(f"Error: {e}")

    print("\nNew traverser after modification (includes new book, skips invalid):")
    for book in lib:
        print(book)
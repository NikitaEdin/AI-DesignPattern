class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

class LibraryCatalog:
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def __len__(self):
        return len(self._books)

    def __iter__(self):
        return self.create_forward_cursor()

    def create_forward_cursor(self):
        return ForwardBookCursor(self._books)

    def create_reverse_cursor(self):
        return ReverseBookCursor(self._books)

class ForwardBookCursor:
    def __init__(self, books):
        self._books = list(books)
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position >= len(self._books):
            raise StopIteration
        current_book = self._books[self._position]
        self._position += 1
        return current_book

    def reset(self):
        self._position = 0

class ReverseBookCursor:
    def __init__(self, books):
        self._books = list(books)
        self._position = len(self._books) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._position < 0:
            raise StopIteration
        current_book = self._books[self._position]
        self._position -= 1
        return current_book

    def reset(self):
        self._position = len(self._books) - 1

if __name__ == "__main__":
    catalog = LibraryCatalog()
    catalog.add_book(Book("1984", "George Orwell"))
    catalog.add_book(Book("Dune", "Frank Herbert"))
    catalog.add_book(Book("Foundation", "Isaac Asimov"))

    print("Forward traversal:")
    for book in catalog:
        print(book)

    print("\nReverse traversal:")
    rev_cursor = catalog.create_reverse_cursor()
    for book in rev_cursor:
        print(book)

    print("\nMultiple independent cursors:")
    cursor1 = catalog.create_forward_cursor()
    cursor2 = catalog.create_forward_cursor()
    print(next(cursor1))
    print(next(cursor2))

    print("\nReset functionality:")
    test_cursor = catalog.create_forward_cursor()
    print(next(test_cursor))
    print(next(test_cursor))
    test_cursor.reset()
    print(next(test_cursor))

    print("\nEmpty catalog handling:")
    empty_catalog = LibraryCatalog()
    cursor = empty_catalog.create_forward_cursor()
    try:
        next(cursor)
    except StopIteration:
        print("Handled empty collection")

    rev_empty = empty_catalog.create_reverse_cursor()
    try:
        next(rev_empty)
    except StopIteration:
        print("Handled empty reverse")
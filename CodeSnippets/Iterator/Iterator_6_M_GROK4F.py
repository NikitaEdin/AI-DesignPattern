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
        if not isinstance(book, Book):
            raise ValueError("Must provide a valid Book instance")
        self.books.append(book)

    def __len__(self):
        return len(self.books)

    def __iter__(self):
        return BookTraverser(self)

class BookTraverser:
    def __init__(self, library):
        self.library = library
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.library):
            raise StopIteration
        book = self.library.books[self.current_index]
        self.current_index += 1
        return book

if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("Python Basics", "John Doe"))
    lib.add_book(Book("Advanced Python", "Jane Smith"))
    lib.add_book(Book("Data Structures", "Alice Johnson"))

    print("Library contents:")
    for book in lib:
        print(book)
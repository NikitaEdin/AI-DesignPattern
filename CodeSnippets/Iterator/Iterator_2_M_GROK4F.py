class Book:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if not isinstance(book, Book):
            raise ValueError("Must add a Book instance")
        self.books.append(book)

    def __iter__(self):
        return BookReader(self.books)

class BookReader:
    def __init__(self, books):
        self.books = books
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.books):
            raise StopIteration
        book = self.books[self.current_index]
        self.current_index += 1
        return book

if __name__ == "__main__":
    library = Library()
    library.add_book(Book("Python Basics", "Programming"))
    library.add_book(Book("Data Structures", "Computer Science"))
    library.add_book(Book("Design Patterns", "Software Engineering"))

    print("Library books:")
    for book in library:
        print(f"- {book.title} ({book.genre})")
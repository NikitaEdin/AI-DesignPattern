class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if book is None:
            raise ValueError("Book cannot be None")
        self.books.append(book)

    def create_browser(self):
        return BookBrowser(self)

class BookBrowser:
    def __init__(self, library):
        self.library = library
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.library.books):
            raise StopIteration
        book = self.library.books[self.current_index]
        self.current_index += 1
        return book

    def reset(self):
        self.current_index = 0

def main():
    lib = Library()
    lib.add_book(Book("1984", "George Orwell"))
    lib.add_book(Book("Brave New World", "Aldous Huxley"))
    lib.add_book(Book("Fahrenheit 451", "Ray Bradbury"))

    browser = lib.create_browser()
    print("First pass:")
    for book in browser:
        print(f"{book.title} by {book.author}")

    browser.reset()
    print("\nSecond pass after reset:")
    for book in browser:
        print(f"{book.title} by {book.author}")

if __name__ == "__main__":
    main()
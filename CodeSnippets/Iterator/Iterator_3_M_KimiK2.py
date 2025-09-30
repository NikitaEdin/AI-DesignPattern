class Book:
    def __init__(self, title):
        self.title = title

class Library:
    def __init__(self):
        self._books = []
    def add_book(self, book):
        self._books.append(book)
    def __iter__(self):
        return LibraryBrowse(self._books)

class LibraryBrowse:
    def __init__(self, books):
        self._books = books
        self._index = 0
    def __next__(self):
        if self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            return book
        raise StopIteration

if __name__ == "__main__":
    lib = Library()
    for title in ["1984", "Brave New World", "Fahrenheit 451"]:
        lib.add_book(Book(title))
    for book in lib:
        print(book.title)
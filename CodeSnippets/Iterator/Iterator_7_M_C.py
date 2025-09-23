class BookCollection:
    def __init__(self):
        self._books = []
    
    def add_book(self, book):
        self._books.append(book)
    
    def create_traverser(self, reverse=False):
        return BookTraverser(self._books, reverse)

class BookTraverser:
    def __init__(self, books, reverse=False):
        self._books = books
        self._reverse = reverse
        self._position = len(books) - 1 if reverse else 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.has_next():
            current_book = self._books[self._position]
            if self._reverse:
                self._position -= 1
            else:
                self._position += 1
            return current_book
        else:
            raise StopIteration
    
    def has_next(self):
        if self._reverse:
            return self._position >= 0
        else:
            return self._position < len(self._books)
    
    def current(self):
        if 0 <= self._position < len(self._books):
            return self._books[self._position]
        return None

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def __str__(self):
        return f"{self.title} by {self.author}"

if __name__ == "__main__":
    library = BookCollection()
    library.add_book(Book("1984", "George Orwell"))
    library.add_book(Book("Brave New World", "Aldous Huxley"))
    library.add_book(Book("Fahrenheit 451", "Ray Bradbury"))
    
    print("Forward traversal:")
    for book in library.create_traverser():
        print(book)
    
    print("\nReverse traversal:")
    for book in library.create_traverser(reverse=True):
        print(book)
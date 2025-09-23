class BookCollection:
    def __init__(self):
        self._books = []
    
    def add_book(self, title, author):
        self._books.append({'title': title, 'author': author})
    
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
        try:
            if self._reverse:
                if self._position < 0:
                    raise StopIteration
                book = self._books[self._position]
                self._position -= 1
            else:
                if self._position >= len(self._books):
                    raise StopIteration
                book = self._books[self._position]
                self._position += 1
            return book
        except IndexError:
            raise StopIteration
    
    def has_next(self):
        if self._reverse:
            return self._position >= 0
        return self._position < len(self._books)

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("Brave New World", "Aldous Huxley")
    library.add_book("Fahrenheit 451", "Ray Bradbury")
    
    print("Forward traversal:")
    for book in library.create_traverser():
        print(f"{book['title']} by {book['author']}")
    
    print("\nReverse traversal:")
    for book in library.create_traverser(reverse=True):
        print(f"{book['title']} by {book['author']}")
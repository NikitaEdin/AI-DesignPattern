class BookCollection:
    def __init__(self):
        self._books = []
    
    def add_book(self, title, author):
        self._books.append({"title": title, "author": author})
    
    def create_traverser(self):
        return BookTraverser(self._books)
    
    def create_reverse_traverser(self):
        return ReverseBookTraverser(self._books)

class BookTraverser:
    def __init__(self, books):
        self._books = books
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book

class ReverseBookTraverser:
    def __init__(self, books):
        self._books = books
        self._index = len(books) - 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < 0:
            raise StopIteration
        book = self._books[self._index]
        self._index -= 1
        return book

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("Brave New World", "Aldous Huxley")
    library.add_book("Fahrenheit 451", "Ray Bradbury")
    
    print("Forward traversal:")
    for book in library.create_traverser():
        print(f"{book['title']} by {book['author']}")
    
    print("\nReverse traversal:")
    for book in library.create_reverse_traverser():
        print(f"{book['title']} by {book['author']}")
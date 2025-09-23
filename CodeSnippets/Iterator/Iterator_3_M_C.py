class BookCollection:
    def __init__(self):
        self._books = []
        self._index = 0
    
    def add_book(self, title, author):
        self._books.append({"title": title, "author": author})
    
    def __iter__(self):
        return BookTraverser(self._books)
    
    def __len__(self):
        return len(self._books)

class BookTraverser:
    def __init__(self, books):
        self._books = books
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position >= len(self._books):
            raise StopIteration
        
        current_book = self._books[self._position]
        self._position += 1
        return current_book
    
    def has_next(self):
        return self._position < len(self._books)
    
    def reset(self):
        self._position = 0

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("To Kill a Mockingbird", "Harper Lee")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    
    print(f"Library contains {len(library)} books:")
    
    for book in library:
        print(f"- {book['title']} by {book['author']}")
    
    print("\nManual traversal:")
    traverser = BookTraverser(library._books)
    while traverser.has_next():
        book = next(traverser)
        print(f"Reading: {book['title']}")
    
    traverser.reset()
    first_book = next(traverser)
    print(f"\nFirst book after reset: {first_book['title']}")
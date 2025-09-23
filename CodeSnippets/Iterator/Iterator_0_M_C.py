class BookCollection:
    def __init__(self):
        self._books = []
        self._current = 0
    
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
        
        book = self._books[self._position]
        self._position += 1
        return book
    
    def has_next(self):
        return self._position < len(self._books)
    
    def reset(self):
        self._position = 0

class FilteredTraverser:
    def __init__(self, books, author_filter=None):
        self._books = books
        self._author_filter = author_filter
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self._position < len(self._books):
            book = self._books[self._position]
            self._position += 1
            
            if self._author_filter is None or book["author"] == self._author_filter:
                return book
        
        raise StopIteration

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("Animal Farm", "George Orwell")
    library.add_book("To Kill a Mockingbird", "Harper Lee")
    
    for book in library:
        print(f"{book['title']} by {book['author']}")
    
    print("\nFiltered by George Orwell:")
    orwell_books = FilteredTraverser(library._books, "George Orwell")
    for book in orwell_books:
        print(f"{book['title']} by {book['author']}")
class BookCollection:
    def __init__(self):
        self._books = []
        self._index = 0
    
    def add_book(self, title, author):
        self._books.append({'title': title, 'author': author})
    
    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book
    
    def __len__(self):
        return len(self._books)
    
    def get_by_author(self, author):
        return AuthorFilter(self._books, author)

class AuthorFilter:
    def __init__(self, books, target_author):
        self._books = books
        self._target_author = target_author
        self._index = 0
    
    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        while self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            if book['author'].lower() == self._target_author.lower():
                return book
        raise StopIteration

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("Animal Farm", "George Orwell")
    library.add_book("To Kill a Mockingbird", "Harper Lee")
    library.add_book("Brave New World", "Aldous Huxley")
    
    print("All books:")
    for book in library:
        print(f"- {book['title']} by {book['author']}")
    
    print("\nBooks by George Orwell:")
    for book in library.get_by_author("George Orwell"):
        print(f"- {book['title']}")
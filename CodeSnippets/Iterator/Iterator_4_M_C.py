class BookCollection:
    def __init__(self):
        self._books = []
        self._filter_genre = None
    
    def add_book(self, title, author, genre):
        self._books.append({"title": title, "author": author, "genre": genre})
    
    def set_genre_filter(self, genre):
        self._filter_genre = genre
    
    def clear_filter(self):
        self._filter_genre = None
    
    def __iter__(self):
        return BookTraverser(self._books, self._filter_genre)

class BookTraverser:
    def __init__(self, books, filter_genre=None):
        self._books = books
        self._filter_genre = filter_genre
        self._index = 0
        self._filtered_books = self._apply_filter()
    
    def _apply_filter(self):
        if self._filter_genre:
            return [book for book in self._books if book["genre"].lower() == self._filter_genre.lower()]
        return self._books
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._filtered_books):
            raise StopIteration
        
        book = self._filtered_books[self._index]
        self._index += 1
        return book

if __name__ == "__main__":
    library = BookCollection()
    
    library.add_book("1984", "George Orwell", "Science Fiction")
    library.add_book("To Kill a Mockingbird", "Harper Lee", "Fiction")
    library.add_book("Dune", "Frank Herbert", "Science Fiction")
    library.add_book("The Catcher in the Rye", "J.D. Salinger", "Fiction")
    
    print("All books:")
    for book in library:
        print(f"- {book['title']} by {book['author']}")
    
    print("\nScience Fiction books only:")
    library.set_genre_filter("Science Fiction")
    for book in library:
        print(f"- {book['title']} by {book['author']}")
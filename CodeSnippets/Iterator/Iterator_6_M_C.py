class BookShelf:
    def __init__(self):
        self._books = []
    
    def add_book(self, book):
        self._books.append(book)
    
    def remove_book(self, book):
        if book in self._books:
            self._books.remove(book)
    
    def get_navigator(self):
        return BookNavigator(self._books)
    
    def get_reverse_navigator(self):
        return ReverseBookNavigator(self._books)

class BookNavigator:
    def __init__(self, books):
        self._books = books
        self._position = 0
    
    def has_next(self):
        return self._position < len(self._books)
    
    def next(self):
        if not self.has_next():
            raise StopIteration("No more books available")
        book = self._books[self._position]
        self._position += 1
        return book

class ReverseBookNavigator:
    def __init__(self, books):
        self._books = books
        self._position = len(books) - 1
    
    def has_next(self):
        return self._position >= 0
    
    def next(self):
        if not self.has_next():
            raise StopIteration("No more books available")
        book = self._books[self._position]
        self._position -= 1
        return book

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Python Programming")
    shelf.add_book("Design Patterns")
    shelf.add_book("Data Structures")
    
    print("Forward navigation:")
    navigator = shelf.get_navigator()
    while navigator.has_next():
        print(navigator.next())
    
    print("\nReverse navigation:")
    reverse_nav = shelf.get_reverse_navigator()
    while reverse_nav.has_next():
        print(reverse_nav.next())
class BookShelf:
    def __init__(self):
        self._books = []
    
    def add_book(self, title):
        self._books.append(title)
    
    def create_browse(self):
        return BookBrowse(self)
    
    def __len__(self):
        return len(self._books)
    
    def get_book(self, index):
        if 0 <= index < len(self._books):
            return self._books[index]
        raise IndexError("Index out of range")

class BookBrowse:
    def __init__(self, shelf):
        self._shelf = shelf
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position < len(self._shelf):
            book = self._shelf.get_book(self._position)
            self._position += 1
            return book
        raise StopIteration

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("1984")
    shelf.add_book("Brave New World")
    shelf.add_book("Fahrenheit 451")
    
    browse = shelf.create_browse()
    for book in browse:
        print(book)
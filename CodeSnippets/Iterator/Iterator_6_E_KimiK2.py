class BookShelf:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def __iter__(self):
        return BookShelfCursor(self.books)

class BookShelfCursor:
    def __init__(self, books):
        self.books = books
        self.index = 0
    
    def __next__(self):
        if self.index >= len(self.books):
            raise StopIteration
        book = self.books[self.index]
        self.index += 1
        return book

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Book A")
    shelf.add_book("Book B")
    shelf.add_book("Book C")
    
    for book in shelf:
        print(book)
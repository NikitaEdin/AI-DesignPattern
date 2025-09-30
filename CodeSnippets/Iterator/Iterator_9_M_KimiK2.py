class BookShelf:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def __iter__(self):
        return BookShelfTraversal(self)


class BookShelfTraversal:
    def __init__(self, bookshelf):
        self.bookshelf = bookshelf
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.bookshelf.books):
            raise StopIteration
        book = self.bookshelf.books[self.index]
        self.index += 1
        return book


class Book:
    def __init__(self, title):
        self.title = title
    
    def __str__(self):
        return self.title


if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("1984"))
    shelf.add_book(Book("Brave New World"))
    shelf.add_book(Book("Fahrenheit 451"))
    
    for book in shelf:
        print(book)
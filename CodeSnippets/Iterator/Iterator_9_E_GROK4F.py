class BookShelf:
    def __init__(self):
        self.books = []
        self.current_index = 0

    def add_book(self, book):
        self.books.append(book)

    def create_traversal(self):
        return BookShelfTraversal(self)

class BookShelfTraversal:
    def __init__(self, shelf):
        self.shelf = shelf
        self.current_index = 0

    def has_next(self):
        return self.current_index < len(self.shelf.books)

    def next_book(self):
        if self.has_next():
            book = self.shelf.books[self.current_index]
            self.current_index += 1
            return book
        raise StopIteration

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Book One")
    shelf.add_book("Book Two")
    shelf.add_book("Book Three")
    traversal = shelf.create_traversal()
    while traversal.has_next():
        print(traversal.next_book())
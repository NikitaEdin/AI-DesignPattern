class BookCollection:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def create_traverser(self):
        return BookTraverser(self.books)

class BookTraverser:
    def __init__(self, books):
        self.books = books
        self.position = 0
    
    def has_next(self):
        return self.position < len(self.books)
    
    def next(self):
        if self.has_next():
            book = self.books[self.position]
            self.position += 1
            return book
        return None

if __name__ == "__main__":
    collection = BookCollection()
    collection.add_book("Python Guide")
    collection.add_book("Design Patterns")
    collection.add_book("Clean Code")
    
    traverser = collection.create_traverser()
    while traverser.has_next():
        print(traverser.next())
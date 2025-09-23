class Book:
    def __init__(self, title):
        self.title = title

class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if not isinstance(book, Book):
            raise ValueError("Must add Book instances only")
        self.books.append(book)

    def __iter__(self):
        return BookTraverser(self.books)

class BookTraverser:
    def __init__(self, books):
        self.books = books
        self.current_position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_position >= len(self.books):
            raise StopIteration
        current_book = self.books[self.current_position]
        self.current_position += 1
        return current_book

    def reset(self):
        self.current_position = 0

if __name__ == "__main__":
    collection = BookCollection()
    collection.add_book(Book("The Great Gatsby"))
    collection.add_book(Book("1984"))
    collection.add_book(Book("To Kill a Mockingbird"))

    traverser = iter(collection)
    print(next(traverser).title)

    for book in collection:
        print(book.title)

    traverser.reset()
    print("After reset:")
    print(next(traverser).title)
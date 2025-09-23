class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_traverser(self, reverse=False):
        return ShelfTraverser(self.books, reverse)


class ShelfTraverser:
    def __init__(self, books, reverse=False):
        self.books = books
        self.reverse = reverse
        self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        if self.reverse:
            if self.current_index < 0:
                raise StopIteration
        else:
            if self.current_index >= len(self.books):
                raise StopIteration

        book = self.books[self.current_index]
        self.current_index += -1 if self.reverse else 1
        return book

    def reset(self):
        self.current_index = len(self.books) - 1 if self.reverse else 0


if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald"))
    shelf.add_book(Book("1984", "George Orwell"))
    shelf.add_book(Book("To Kill a Mockingbird", "Harper Lee"))

    print("Forward traversal:")
    for book in shelf.create_traverser():
        print(book)

    print("\nReverse traversal:")
    traverser = shelf.create_traverser(reverse=True)
    for book in traverser:
        print(book)

    print("\nReset and reverse again:")
    traverser.reset()
    for book in traverser:
        print(book)

    print("\nEmpty shelf:")
    empty_shelf = BookShelf()
    for book in empty_shelf.create_traverser():
        print(book)
class Book:
    def __init__(self, title):
        self.title = title

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_navigator(self):
        return BookNavigator(self)

class BookNavigator:
    def __init__(self, library):
        self.books = library.books
        self.index = -1
        self.current = None

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        self.index += 1
        self.current = self.books[self.index]
        return self.current

    def reset(self):
        self.index = -1
        self.current = None

    def has_next(self):
        return self.index + 1 < len(self.books)

    def has_previous(self):
        return self.index - 1 >= 0

    def get_current(self):
        return self.current

    def step_forward(self):
        if not self.has_next():
            return None
        self.index += 1
        self.current = self.books[self.index]
        return self.current

    def step_backward(self):
        if not self.has_previous():
            return None
        self.index -= 1
        self.current = self.books[self.index]
        return self.current

if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("Book1"))
    lib.add_book(Book("Book2"))
    nav = lib.create_navigator()
    print(nav.has_next())
    book = nav.step_forward()
    print(book.title)
    print(nav.get_current().title)
    print(nav.has_previous())
    book = nav.step_forward()
    print(book.title)
    print(nav.get_current().title)
    print(nav.has_previous())
    book = nav.step_backward()
    print(book.title)
    print(nav.get_current().title)
    print(nav.has_next())
    nav.reset()
    print("First traversal:")
    for book in nav:
        print(book.title)
    print("Second traversal:")
    for book in nav:
        print(book.title)
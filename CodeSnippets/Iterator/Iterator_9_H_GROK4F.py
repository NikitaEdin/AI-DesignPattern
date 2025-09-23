class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookCollection:
    def __init__(self):
        self._books = []

    def add(self, book):
        self._books.append(book)

    def __len__(self):
        return len(self._books)

    def create_selector(self):
        return BookSelector(self._books)

class BookSelector:
    def __init__(self, books):
        self._books = books
        self._current = 0

    def first(self):
        if self._books:
            self._current = 0
        return self.current()

    def last(self):
        if self._books:
            self._current = len(self._books) - 1
        return self.current()

    def next(self):
        if self.has_next():
            self._current += 1
            return self.current()
        return None

    def previous(self):
        if self.has_previous():
            self._current -= 1
            return self.current()
        return None

    def has_next(self):
        return 0 <= self._current < len(self._books) - 1

    def has_previous(self):
        return 0 < self._current <= len(self._books) - 1

    def current(self):
        if 0 <= self._current < len(self._books):
            return self._books[self._current]
        return None

    def remove_current(self):
        if self.current() is not None:
            del self._books[self._current]
            self._current = max(0, self._current - 1)
            return True
        return False

    def __iter__(self):
        self.first()
        return self

    def __next__(self):
        item = self.next()
        if item is None:
            raise StopIteration
        return item

if __name__ == "__main__":
    collection = BookCollection()
    collection.add(Book("The Great Gatsby", "F. Scott Fitzgerald"))
    collection.add(Book("1984", "George Orwell"))
    collection.add(Book("To Kill a Mockingbird", "Harper Lee"))

    print("Forward traversal:")
    selector = collection.create_selector()
    for book in selector:
        print(book)

    print("\nBidirectional demo:")
    selector.first()
    print("Starting forward:")
    while selector.has_next():
        print(selector.next())
    print("Now backward:")
    while selector.has_previous():
        print(selector.previous())

    print("\nRemove middle book and continue:")
    selector = collection.create_selector()
    selector.first()
    print(f"Current: {selector.current()}")
    selector.next()
    print(f"Before remove: {selector.current()}")
    selector.remove_current()
    print(f"After remove: {selector.current()}")
    print(f"Collection size: {len(collection)}")

    print("\nEmpty collection:")
    empty_collection = BookCollection()
    empty_selector = empty_collection.create_selector()
    print(f"Current: {empty_selector.current()}")
    print(f"Has next: {empty_selector.has_next()}")
    print(f"Has previous: {empty_selector.has_previous()}")
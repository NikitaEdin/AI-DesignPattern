class BookShelf:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        if isinstance(title, str) and title.strip():
            self.books.append(title)
        else:
            raise ValueError("Invalid book title")

    def __iter__(self):
        return BookReader(self.books)

class BookReader:
    def __init__(self, books):
        self.books = books
        self.position = 0
        self.total = len(books)

    def __iter__(self):
        return self

    def __next__(self):
        if self.position < self.total:
            current = self.books[self.position]
            self.position += 1
            return current
        raise StopIteration

    def reset(self):
        self.position = 0

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book("Python Basics")
    shelf.add_book("Advanced Algorithms")
    shelf.add_book("Data Structures")

    print("Original order:")
    for title in shelf:
        print(title)

    reader = iter(shelf)
    next(reader)
    print("\nAfter skipping first:")
    for title in reader:
        print(title)

    reader.reset()
    print("\nReset and full traversal:")
    for title in reader:
        print(title)
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def __str__(self):
        return f"{self.title} by {self.author}"

class BookShelf:
    def __init__(self):
        self._books = []
    def add_book(self, book):
        self._books.append(book)
    def __len__(self):
        return len(self._books)
    def __getitem__(self, index):
        if 0 <= index < len(self._books):
            return self._books[index]
        raise IndexError("Index out of range")
    def create_reader(self):
        return BookReader(self)

class BookReader:
    def __init__(self, shelf):
        self._shelf = shelf
        self._pos = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._pos < len(self._shelf):
            book = self._shelf[self._pos]
            self._pos += 1
            return book
        raise StopIteration

if __name__ == "__main__":
    shelf = BookShelf()
    shelf.add_book(Book("1984", "George Orwell"))
    shelf.add_book(Book("Brave New World", "Aldous Huxley"))
    reader = shelf.create_reader()
    for book in reader:
        print(book)
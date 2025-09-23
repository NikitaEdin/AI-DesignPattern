class BookCollection:
    def __init__(self, books):
        self._books = books
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book

class Book:
    def __init__(self, title, author, publication_date):
        self.title = title
        self.author = author
        self.publication_date = publication_date

books = [Book("The Catcher in the Rye", "J.D. Salinger", 1951), Book("To Kill a Mockingbird", "Harper Lee", 1960), Book("1984", "George Orwell", 1949)]

collection = BookCollection(books)
for book in collection:
    print(book.title, book.author, book.publication_date)
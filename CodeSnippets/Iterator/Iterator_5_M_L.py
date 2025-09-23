class BookShelf:
    def __init__(self, books):
        self.books = books

    def __iter__(self):
        return BookShelfIterator(self)

class BookShelfIterator:
    def __init__(self, book_shelf):
        self.book_shelf = book_shelf
        self.current_index = 0

    def __next__(self):
        if self.current_index < len(self.book_shelf.books):
            current_book = self.book_shelf.books[self.current_index]
            self.current_index += 1
            return current_book
        else:
            raise StopIteration

def main():
    book_shelf = BookShelf(["To Kill a Mockingbird", "The Great Gatsby"])
    for book in book_shelf:
        print(book)

if __name__ == "__main__":
    main()
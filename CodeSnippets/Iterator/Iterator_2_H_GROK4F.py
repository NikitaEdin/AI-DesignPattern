class Book:
    def __init__(self, title):
        self.title = title

class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_forward_traverser(self):
        return ForwardTraverser(self)

    def create_reverse_traverser(self):
        return ReverseTraverser(self)

    def size(self):
        return len(self.books)

class ForwardTraverser:
    def __init__(self, collection):
        self.collection = collection
        self.current_index = 0

    def has_more(self):
        return self.current_index < self.collection.size()

    def get_next(self):
        if self.has_more():
            book = self.collection.books[self.current_index]
            self.current_index += 1
            return book
        return None

    def reset(self):
        self.current_index = 0

class ReverseTraverser:
    def __init__(self, collection):
        self.collection = collection
        self.current_index = collection.size() - 1 if collection.size() > 0 else -1

    def has_more(self):
        return self.current_index >= 0

    def get_next(self):
        if self.has_more():
            book = self.collection.books[self.current_index]
            self.current_index -= 1
            return book
        return None

    def reset(self):
        self.current_index = self.collection.size() - 1 if self.collection.size() > 0 else -1

if __name__ == "__main__":
    collection = BookCollection()
    collection.add_book(Book("The Great Gatsby"))
    collection.add_book(Book("1984"))
    collection.add_book(Book("To Kill a Mockingbird"))

    print("Forward traversal:")
    traverser = collection.create_forward_traverser()
    while traverser.has_more():
        book = traverser.get_next()
        print(book.title)

    print("\nReverse traversal:")
    traverser = collection.create_reverse_traverser()
    while traverser.has_more():
        book = traverser.get_next()
        print(book.title)

    print("\nForward with reset:")
    traverser = collection.create_forward_traverser()
    traverser.reset()
    book = traverser.get_next()
    print(f"First book: {book.title}")
    traverser.reset()
    print("Reset complete.")

    # Edge case: empty collection
    empty_collection = BookCollection()
    empty_traverser = empty_collection.create_forward_traverser()
    print(f"\nEmpty collection has more: {empty_traverser.has_more()}")
    print(f"Next from empty: {empty_traverser.get_next()}")
class BookCollection:
    def __init__(self):
        self._books = []
        self._genres = {}
    
    def add_book(self, title, author, genre, year):
        book = {'title': title, 'author': author, 'genre': genre, 'year': year}
        self._books.append(book)
        if genre not in self._genres:
            self._genres[genre] = []
        self._genres[genre].append(book)
    
    def __iter__(self):
        return BookTraverser(self._books)
    
    def traverse_by_genre(self, genre):
        return BookTraverser(self._genres.get(genre, []))
    
    def traverse_by_year_range(self, start_year, end_year):
        filtered_books = [book for book in self._books 
                         if start_year <= book['year'] <= end_year]
        return BookTraverser(filtered_books)
    
    def traverse_reverse(self):
        return BookTraverser(self._books[::-1])


class BookTraverser:
    def __init__(self, books):
        self._books = books
        self._index = 0
        self._snapshot = list(books)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._snapshot):
            raise StopIteration
        book = self._snapshot[self._index]
        self._index += 1
        return book
    
    def peek(self):
        if self._index >= len(self._snapshot):
            return None
        return self._snapshot[self._index]
    
    def has_next(self):
        return self._index < len(self._snapshot)
    
    def reset(self):
        self._index = 0
    
    def skip(self, count=1):
        self._index = min(self._index + count, len(self._snapshot))


class LazySequence:
    def __init__(self, generator_func, *args, **kwargs):
        self._generator_func = generator_func
        self._args = args
        self._kwargs = kwargs
    
    def __iter__(self):
        return LazyTraverser(self._generator_func(*self._args, **self._kwargs))


class LazyTraverser:
    def __init__(self, generator):
        self._generator = generator
        self._cached_items = []
        self._exhausted = False
    
    def __iter__(self):
        for item in self._cached_items:
            yield item
        
        if not self._exhausted:
            try:
                while True:
                    item = next(self._generator)
                    self._cached_items.append(item)
                    yield item
            except StopIteration:
                self._exhausted = True
    
    def __next__(self):
        try:
            return next(iter(self))
        except StopIteration:
            raise


def fibonacci_generator(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1


if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell", "Dystopian", 1949)
    library.add_book("Dune", "Frank Herbert", "Sci-Fi", 1965)
    library.add_book("Foundation", "Isaac Asimov", "Sci-Fi", 1951)
    library.add_book("Brave New World", "Aldous Huxley", "Dystopian", 1932)
    
    print("All books:")
    for book in library:
        print(f"  {book['title']} ({book['year']})")
    
    print("\nSci-Fi books:")
    sci_fi_traverser = library.traverse_by_genre("Sci-Fi")
    while sci_fi_traverser.has_next():
        book = next(sci_fi_traverser)
        print(f"  {book['title']} - {book['author']}")
        if sci_fi_traverser.peek():
            print(f"    Next: {sci_fi_traverser.peek()['title']}")
    
    print("\nBooks from 1940-1970:")
    for book in library.traverse_by_year_range(1940, 1970):
        print(f"  {book['title']} ({book['year']})")
    
    print("\nLazy Fibonacci sequence (first 8):")
    fib_sequence = LazySequence(fibonacci_generator, 8)
    for num in fib_sequence:
        print(f"  {num}")
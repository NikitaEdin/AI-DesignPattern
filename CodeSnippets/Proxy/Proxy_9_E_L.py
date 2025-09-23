class BookProxy:
    def __init__(self, book):
        self.book = book
    
    def get_title(self):
        return self.book.title
    
    def get_author(self):
        return self.book.author
    
    def get_publisher(self):
        return self.book.publisher
    
    def __str__(self):
        return f"{self.get_title()} by {self.get_author()} published by {self.get_publisher()}"

class Book:
    def __init__(self, title, author, publisher):
        self.title = title
        self.author = author
        self.publisher = publisher
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_publisher(self):
        return self.publisher

# Usage example
book = Book("The Great Gatsby", "F. Scott Fitzgerald", "Random House")
proxy = BookProxy(book)
print(proxy)
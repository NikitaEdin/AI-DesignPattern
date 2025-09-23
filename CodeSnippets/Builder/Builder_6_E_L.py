# Simple Builder Design Pattern Implementation in Python
class DocumentBuilder:
    def __init__(self):
        self.title = None
        self.author = None
        self.body = None
    
    def with_title(self, title):
        self.title = title
        return self
    
    def with_author(self, author):
        self.author = author
        return self
    
    def with_body(self, body):
        self.body = body
        return self
    
    def build(self):
        return {"title": self.title, "author": self.author, "body": self.body}

# Usage Example
document_builder = DocumentBuilder()
document_builder.with_title("My Document").with_author("John Doe").with_body("This is a sample document.").build()
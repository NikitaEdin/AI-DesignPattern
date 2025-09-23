class DocumentBuilder:
    def __init__(self):
        self.title = None
        self.content = None
        self.author = None

    def with_title(self, title):
        self.title = title
        return self

    def with_content(self, content):
        self.content = content
        return self

    def with_author(self, author):
        self.author = author
        return self

    def build(self):
        return Document(title=self.title, content=self.content, author=self.author)

class Document:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def display(self):
        print(f"Title: {self.title}")
        print(f"Content: {self.content}")
        print(f"Author: {self.author}")

# Usage example
document_builder = DocumentBuilder() \
                        .with_title("Python Design Patterns") \
                        .with_content("This is a sample document") \
                        .with_author("John Doe") \
                        .build()

print(document_builder.display())
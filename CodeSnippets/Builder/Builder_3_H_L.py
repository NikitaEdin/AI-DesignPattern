class DocumentBuilder:
    def __init__(self):
        self.title = None
        self.author = None
        self.content = []
    
    def with_title(self, title):
        self.title = title
        return self
    
    def with_author(self, author):
        self.author = author
        return self
    
    def with_content(self, content):
        self.content.append(content)
        return self
    
    def build(self):
        return Document(self.title, self.author, self.content)

class Document:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

def main():
    document_builder = DocumentBuilder()
        .with_title("My Document")
        .with_author("John Doe")
        .with_content("This is the content of my document.")
        .build()
    
    print(document_builder.title) # Output: "My Document"
    print(document_builder.author) # Output: "John Doe"
    print(document_builder.content) # Output: ["This is the content of my document."]
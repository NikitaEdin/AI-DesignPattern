class Document:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

class Builder:
    def __init__(self, document):
        self.document = document

    def set_title(self, title):
        self.document.title = title
        return self

    def set_author(self, author):
        self.document.author = author
        return self

    def build(self):
        return self.document

# Usage example

def main():
    builder = Builder(Document("", ""))
    builder.set_title("The Great Gatsby").set_author("F. Scott Fitzgerald")
    document = builder.build()
    print(f"{document.get_title()} by {document.get_author()}")

if __name__ == "__main__":
    main()
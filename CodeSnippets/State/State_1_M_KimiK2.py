class Mode:
    def handle(self, context):
        raise NotImplementedError
    def __repr__(self):
        return self.__class__.__name__

class Draft(Mode):
    def handle(self, context):
        context.content = "DRAFT: " + context.content
        context.mode = Review()

class Review(Mode):
    def handle(self, context):
        context.content = "REVIEWED: " + context.content
        context.mode = Published()

class Published(Mode):
    def handle(self, context):
        raise RuntimeError("Document already published")

class Document:
    def __init__(self, content):
        self.content = content
        self.mode = Draft()
    def advance(self):
        self.mode.handle(self)
    def __repr__(self):
        return f"Document({self.content}, mode={self.mode})"

if __name__ == "__main__":
    doc = Document("Initial draft")
    print(doc)
    doc.advance()
    print(doc)
    doc.advance()
    print(doc)
    try:
        doc.advance()
    except RuntimeError as e:
        print("Error:", e)
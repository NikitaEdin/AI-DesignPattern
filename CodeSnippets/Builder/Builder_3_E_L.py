class Director:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_preamble()
        self.builder.build_body()
        self.builder.build_postscript()

class DocumentBuilder:
    def build_preamble(self):
        print("Preamble")

    def build_body(self):
        print("Body")

    def build_postscript(self):
        print("Postscript")

if __name__ == "__main__":
    builder = DocumentBuilder()
    director = Director(builder)
    director.construct()
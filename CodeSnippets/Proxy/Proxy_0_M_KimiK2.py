class Document:
    def __init__(self, filename):
        self.filename = filename
        self._content = None

    def read(self):
        if self._content is None:
            with open(self.filename) as f:
                self._content = f.read()
        return self._content


class SecureDocument:
    def __init__(self, filename, password):
        self._document = Document(filename)
        self._password = password
        self._authenticated = False

    def authenticate(self, password):
        self._authenticated = (password == self._password)

    def read(self):
        if not self._authenticated:
            raise PermissionError("Access denied: invalid credentials")
        return self._document.read()


if __name__ == "__main__":
    doc = SecureDocument("example.txt", "secret123")
    try:
        print(doc.read())
    except PermissionError as e:
        print(e)

    doc.authenticate("secret123")
    try:
        print(doc.read())
    except FileNotFoundError:
        print("File not found")
class Connection:
    def __init__(self):
        self._handler = ClosedHandler()

    def open(self):
        self._handler.open(self)

    def close(self):
        self._handler.close(self)

    def set_handler(self, handler):
        self._handler = handler

class Handler:
    def open(self, conn):
        pass

    def close(self, conn):
        pass

class ClosedHandler(Handler):
    def open(self, conn):
        print("Opening connection")
        conn.set_handler(OpenHandler())

    def close(self, conn):
        print("Already closed")

class OpenHandler(Handler):
    def open(self, conn):
        print("Already open")

    def close(self, conn):
        print("Closing connection")
        conn.set_handler(ClosedHandler())

if __name__ == "__main__":
    c = Connection()
    c.open()
    c.close()
    c.open()
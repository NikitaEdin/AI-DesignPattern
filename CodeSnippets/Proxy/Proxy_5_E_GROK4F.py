class RealDatabase:
    def __init__(self):
        print("Connecting to database...")

    def query(self, sql):
        print(f"Executing: {sql}")

class DatabaseAccess:
    def __init__(self):
        self._db = None

    def query(self, sql):
        if self._db is None:
            self._db = RealDatabase()
        self._db.query(sql)

if __name__ == "__main__":
    access = DatabaseAccess()
    access.query("SELECT * FROM users")
    access.query("SELECT * FROM posts")
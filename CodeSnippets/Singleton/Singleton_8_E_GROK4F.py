class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.value = "Database connected"
            self._initialized = True

if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    print(db1 is db2)
    print(db1.value)
    print(db2.value)
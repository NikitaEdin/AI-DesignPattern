class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Database connected"
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.status = "Ready"
            self._initialized = True

if __name__ == "__main__":
    first = DatabaseManager()
    second = DatabaseManager()
    print(first.connection)
    print(second.connection)
    print(first is second)
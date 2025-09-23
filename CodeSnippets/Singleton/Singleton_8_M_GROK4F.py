class DatabaseManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.is_connected = False
            self.connection = None

    def connect(self):
        if self.is_connected:
            print("Already connected.")
            return
        self.connection = "Database connection established"
        self.is_connected = True
        print(self.connection)

    def query(self, sql_statement):
        if not self.is_connected:
            raise ValueError("Database not connected. Call connect() first.")
        print(f"Executing query: {sql_statement}")
        return f"Results from: {sql_statement}"

    def disconnect(self):
        if not self.is_connected:
            print("Not connected.")
            return
        self.is_connected = False
        self.connection = None
        print("Database disconnected.")

if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    print(f"Same instance: {db1 is db2}")
    db1.connect()
    result1 = db1.query("SELECT * FROM users")
    print(result1)
    db2.query("SELECT * FROM products")
    db1.disconnect()
    try:
        db2.query("SELECT * FROM orders")
    except ValueError as e:
        print(f"Error: {e}")
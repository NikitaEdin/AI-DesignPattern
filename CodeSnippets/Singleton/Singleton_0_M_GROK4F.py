class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connected = False
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        print("Establishing connection to database...")
        self._connected = True
        self._host = "localhost"
        self._port = 5432

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    def query(self, sql_statement):
        if not self._connected:
            raise ConnectionError("Database connection is not active.")
        result = f"Query executed on {self._host}:{self._port}: {sql_statement}"
        print(result)
        return result

    def disconnect(self):
        if self._connected:
            print("Closing database connection...")
            self._connected = False

if __name__ == "__main__":
    conn1 = DatabaseConnection()
    conn1.query("SELECT * FROM users")

    conn2 = DatabaseConnection()
    print(f"Same connection: {conn1 is conn2}")

    conn2.query("INSERT INTO logs VALUES ('test')")

    try:
        conn1.disconnect()
        conn1.query("SELECT * FROM status")
    except ConnectionError as e:
        print(f"Error: {e}")

    conn1._connect()
    conn1.query("SELECT * FROM status")
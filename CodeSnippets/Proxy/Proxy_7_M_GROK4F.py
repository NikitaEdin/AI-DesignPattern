class DatabaseService:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        if not conn_str or not isinstance(conn_str, str):
            raise ValueError("Invalid connection string")
        self._connect()

    def _connect(self):
        print(f"Establishing connection to {self.conn_str}")

    def execute(self, query):
        print(f"Executing: {query}")
        return f"Results from {query}"

class ConnectionManager:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self._service = None

    def execute(self, query):
        if self._service is None:
            self._service = DatabaseService(self.conn_str)
        return self._service.execute(query)

if __name__ == "__main__":
    mgr = ConnectionManager("mysql://localhost/mydb")
    result = mgr.execute("SELECT * FROM users")
    print(result)
    result2 = mgr.execute("SELECT * FROM orders")
    print(result2)
    try:
        mgr_invalid = ConnectionManager("")
        mgr_invalid.execute("SELECT * FROM test")
    except ValueError as e:
        print(f"Error: {e}")
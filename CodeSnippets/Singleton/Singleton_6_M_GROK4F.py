class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connection_status = "Disconnected"
            self._query_count = 0

    def connect(self, host="localhost", port=5432):
        try:
            if self._connection_status == "Disconnected":
                self._connection_status = f"Connected to {host}:{port}"
                print(f"Established connection to {host}:{port}")
            else:
                print("Already connected")
        except Exception as e:
            self._connection_status = "Connection failed"
            print(f"Connection error: {e}")

    def execute_query(self, query):
        if self._connection_status.startswith("Connected"):
            self._query_count += 1
            print(f"Executed query: {query} (Query #{self._query_count})")
            return True
        else:
            print("Cannot execute query: Not connected")
            return False

    def get_status(self):
        return {
            "status": self._connection_status,
            "query_count": self._query_count
        }

if __name__ == "__main__":
    manager1 = DatabaseManager()
    manager2 = DatabaseManager()

    print(f"Same instance: {manager1 is manager2}")

    manager1.connect("localhost", 5432)
    print(manager1.get_status())

    manager2.execute_query("SELECT * FROM users")
    print(manager2.get_status())

    manager1.execute_query("UPDATE users SET active = true")
    print(manager1.get_status())
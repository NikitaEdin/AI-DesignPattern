import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, host='localhost', port=5432):
        if self._initialized:
            return
        self.host = host
        self.port = port
        self._connection = None
        self._initialized = True

    def connect(self):
        if self._connection is None:
            self._connection = f"Connected to {self.host}:{self.port}"
        return self._connection

    def query(self, sql):
        if not self._connection:
            raise RuntimeError("Not connected")
        return f"Executed: {sql}"

if __name__ == "__main__":
    conn1 = DatabaseConnection('db1.example.com', 5432)
    conn2 = DatabaseConnection('db2.example.com', 5433)

    print(conn1 is conn2)
    print(conn1.connect())
    print(conn2.connect())

    try:
        print(conn1.query("SELECT * FROM users"))
    except RuntimeError as e:
        print(e)
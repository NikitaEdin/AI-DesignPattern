class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.connection = None
        self.host = "localhost"
        self.port = 5432

    def connect(self):
        if self.connection is not None:
            return False
        try:
            # Simulate connection establishment
            self.connection = f"Connected to {self.host}:{self.port}"
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")

    def disconnect(self):
        if self.connection is None:
            return False
        self.connection = None
        return True

    def is_connected(self):
        return self.connection is not None

    def set_host(self, host):
        if not isinstance(host, str) or not host.strip():
            raise ValueError("Host must be a non-empty string")
        self.host = host.strip()

if __name__ == "__main__":
    manager1 = DatabaseManager()
    manager2 = DatabaseManager()

    print(manager1 is manager2)  # Should be True

    print(manager1.connect())  # True
    print(manager1.is_connected())  # True

    print(manager2.connect())  # False
    print(manager2.is_connected())  # True

    manager1.disconnect()
    print(manager1.is_connected())  # False
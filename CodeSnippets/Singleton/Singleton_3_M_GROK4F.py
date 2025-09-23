class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.status = "idle"
            self.connection_count = 0
            print(f"Initializing {self.__class__.__name__}")

    def connect(self):
        if self.status == "connected":
            return "Already connected"
        try:
            self.status = "connected"
            self.connection_count += 1
            return f"Connected successfully. Total connections: {self.connection_count}"
        except Exception as e:
            self.status = "error"
            return f"Connection failed: {str(e)}"

    def disconnect(self):
        if self.status != "connected":
            return "Not connected"
        self.status = "idle"
        return "Disconnected"

    def get_status(self):
        return self.status

if __name__ == "__main__":
    manager1 = DatabaseManager()
    result1 = manager1.connect()
    print(result1)

    manager2 = DatabaseManager()
    print(f"Same instance: {manager1 is manager2}")
    print(f"Status: {manager2.get_status()}")

    result2 = manager2.disconnect()
    print(result2)

    print(f"Final status: {manager1.get_status()}")
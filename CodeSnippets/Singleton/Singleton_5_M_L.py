class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def connect(self, host, port):
        # Connect to the database here using the host and port parameters
        print(f"Connecting to {host}:{port}")
        self.connection = "Connection established!"

    def disconnect(self):
        # Disconnect from the database here
        print("Disconnecting from the database...")
        del self.connection
    
    @classmethod
    def get_instance(cls, host="localhost", port=5432):
        return cls().connect(host, port)

# Usage example
if __name__ == "__main__":
    db1 = DatabaseConnection.get_instance("db1")
    print(db1.connection)
    db2 = DatabaseConnection.get_instance("db2", 5433)
    print(db2.connection)
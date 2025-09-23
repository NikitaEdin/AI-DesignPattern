class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance
    
    def connect(self):
        if not self.connected:
            self.connected = True
            return "Connected to database"
        return "Already connected"
    
    def get_status(self):
        return "Connected" if self.connected else "Disconnected"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(db1 is db2)
    print(db1.connect())
    print(db2.get_status())
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected to database"
        return cls._instance
    
    def query(self, sql):
        return f"Executing: {sql}"

if __name__ == "__main__":
    db1 = Database()
    db2 = Database()
    
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 connection: {db1.connection}")
    print(f"db2 connection: {db2.connection}")
    print(db1.query("SELECT * FROM users"))
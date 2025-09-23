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
    
    print(db1 is db2)
    print(db1.connection)
    print(db2.query("SELECT * FROM users"))
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = []
            self.initialized = True
    
    def add_record(self, record):
        self.data.append(record)
    
    def get_records(self):
        return self.data

if __name__ == "__main__":
    db1 = Database()
    db2 = Database()
    
    db1.add_record("User 1")
    db2.add_record("User 2")
    
    print(db1.get_records())
    print(db2.get_records())
    print(db1 is db2)
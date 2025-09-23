class Database:
    def connect(self):
        return "Database connected"
    
    def query(self, sql):
        return f"Executing: {sql}"

class Cache:
    def get(self, key):
        return f"Cache hit for {key}"
    
    def set(self, key, value):
        return f"Cached {key}: {value}"

class Logger:
    def log(self, message):
        return f"Logged: {message}"

class DataManager:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()
    
    def get_user(self, user_id):
        self.db.connect()
        cached = self.cache.get(f"user_{user_id}")
        result = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        self.logger.log(f"Retrieved user {user_id}")
        return f"User {user_id} data"

if __name__ == "__main__":
    manager = DataManager()
    user = manager.get_user(123)
    print(user)
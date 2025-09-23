class Database:
    def connect(self):
        return "Database connected"
    
    def query(self, sql):
        return f"Executing: {sql}"

class Cache:
    def get(self, key):
        return f"Cache get: {key}"
    
    def set(self, key, value):
        return f"Cache set: {key} = {value}"

class Logger:
    def log(self, message):
        return f"Log: {message}"

class DataManager:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()
    
    def get_user_data(self, user_id):
        self.db.connect()
        cached = self.cache.get(user_id)
        result = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        self.cache.set(user_id, result)
        self.logger.log(f"Retrieved user {user_id}")
        return result

if __name__ == "__main__":
    manager = DataManager()
    print(manager.get_user_data(123))
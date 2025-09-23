class DatabaseConnection:
    def connect(self):
        return "Database connected"
    
    def execute_query(self, query):
        if not query:
            raise ValueError("Query cannot be empty")
        return f"Executed: {query}"
    
    def disconnect(self):
        return "Database disconnected"

class Logger:
    def log(self, message):
        return f"[LOG] {message}"

class CacheManager:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value

class DataAccessManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.logger = Logger()
        self.cache = CacheManager()
    
    def get_user_data(self, user_id):
        try:
            cached_data = self.cache.get(f"user_{user_id}")
            if cached_data:
                self.logger.log(f"Retrieved user {user_id} from cache")
                return cached_data
            
            self.db.connect()
            query = f"SELECT * FROM users WHERE id = {user_id}"
            result = self.db.execute_query(query)
            self.db.disconnect()
            
            self.cache.set(f"user_{user_id}", result)
            self.logger.log(f"Retrieved user {user_id} from database")
            return result
        
        except Exception as e:
            self.logger.log(f"Error retrieving user {user_id}: {str(e)}")
            return None

if __name__ == "__main__":
    data_manager = DataAccessManager()
    
    print(data_manager.get_user_data(123))
    print(data_manager.get_user_data(123))
    print(data_manager.get_user_data(456))
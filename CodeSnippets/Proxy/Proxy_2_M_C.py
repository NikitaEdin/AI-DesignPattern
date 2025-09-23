class DatabaseService:
    def __init__(self):
        self._connected = False
    
    def connect(self):
        print("Establishing database connection...")
        self._connected = True
    
    def fetch_user_data(self, user_id):
        if not self._connected:
            raise ConnectionError("Database not connected")
        print(f"Fetching user data for ID: {user_id}")
        return {"id": user_id, "name": f"User_{user_id}", "email": f"user{user_id}@example.com"}

class CachedDatabaseAccess:
    def __init__(self):
        self._service = None
        self._cache = {}
    
    def _get_service(self):
        if self._service is None:
            self._service = DatabaseService()
            self._service.connect()
        return self._service
    
    def fetch_user_data(self, user_id):
        if user_id in self._cache:
            print(f"Returning cached data for user ID: {user_id}")
            return self._cache[user_id]
        
        try:
            service = self._get_service()
            data = service.fetch_user_data(user_id)
            self._cache[user_id] = data
            return data
        except ConnectionError as e:
            print(f"Error accessing database: {e}")
            return None

if __name__ == "__main__":
    db_access = CachedDatabaseAccess()
    
    user1 = db_access.fetch_user_data(123)
    print(f"Retrieved: {user1}")
    
    user1_cached = db_access.fetch_user_data(123)
    print(f"Retrieved: {user1_cached}")
    
    user2 = db_access.fetch_user_data(456)
    print(f"Retrieved: {user2}")
class DatabaseInterface:
    def execute_query(self, query):
        pass

class RealDatabase(DatabaseInterface):
    def __init__(self):
        self.connection = "established"

    def execute_query(self, query):
        if not self.connection:
            raise ConnectionError("No connection available")
        return f"Executed: {query} - Results from real database"

class SecureDatabase(DatabaseInterface):
    def __init__(self, real_db, user_role):
        self.real_db = real_db
        self.user_role = user_role
        self._cache = {}

    def execute_query(self, query):
        if self.user_role != "admin" and "delete" in query.lower():
            raise PermissionError("Access denied for this operation")
        
        if query in self._cache:
            return self._cache[query]
        
        result = self.real_db.execute_query(query)
        self._cache[query] = result
        return result

if __name__ == "__main__":
    real_db = RealDatabase()
    secure_db_admin = SecureDatabase(real_db, "admin")
    secure_db_user = SecureDatabase(real_db, "user")
    
    try:
        print(secure_db_admin.execute_query("SELECT * FROM users"))
        print(secure_db_user.execute_query("SELECT * FROM users"))
        secure_db_user.execute_query("DELETE FROM users")
    except PermissionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
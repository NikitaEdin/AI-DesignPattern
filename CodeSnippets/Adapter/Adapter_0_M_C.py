class LegacyPrinter:
    def old_print(self, text):
        return f"LEGACY: {text.upper()}"

class ModernPrinter:
    def print_document(self, content):
        return f"Modern Print: {content}"

class PrinterBridge:
    def __init__(self, legacy_printer):
        self._legacy_printer = legacy_printer
        
    def print_document(self, content):
        if not content:
            raise ValueError("Content cannot be empty")
        return self._legacy_printer.old_print(content)

class DatabaseConnection:
    def fetch_data(self, query):
        return {"id": 1, "name": "John", "email": "john@email.com"}

class APIClient:
    def get_user_info(self, user_id):
        return f"User data for ID: {user_id}"

class DataSourceWrapper:
    def __init__(self, database_connection):
        self._db = database_connection
        
    def get_user_info(self, user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        query = f"SELECT * FROM users WHERE id = {user_id}"
        data = self._db.fetch_data(query)
        return f"User data for ID: {user_id} - {data}"

if __name__ == "__main__":
    legacy = LegacyPrinter()
    modern = ModernPrinter()
    bridge = PrinterBridge(legacy)
    
    print(modern.print_document("Hello World"))
    print(bridge.print_document("Hello World"))
    
    db = DatabaseConnection()
    api = APIClient()
    wrapper = DataSourceWrapper(db)
    
    print(api.get_user_info(123))
    print(wrapper.get_user_info(123))
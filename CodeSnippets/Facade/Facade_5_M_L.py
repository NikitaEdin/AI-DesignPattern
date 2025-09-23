class UserInterface:
    def __init__(self, user_name):
        self.user_name = user_name

    def display_welcome_message(self):
        print(f"Welcome back, {self.user_name}!")

class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url

    def query(self, query_string):
        # Simulate a database query for demonstration purposes
        print("Executing query...")
        return "Query results"

class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_user(self, user_id):
        # Simulate a database query for demonstration purposes
        print("Executing query...")
        return "User data"

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def get_user(self, user_id):
        # Simulate a database query for demonstration purposes
        print("Executing query...")
        return "User data"

class UserApplication:
    def __init__(self, service):
        self.service = service

    def run(self):
        user_id = 1234567890
        user = self.service.get_user(user_id)
        print(f"User data: {user}")

# Usage example
if __name__ == "__main__":
    db_url = "example.com"
    ui = UserInterface("John Doe")
    connection = DatabaseConnection(db_url)
    repository = UserRepository(connection)
    service = UserService(repository)
    app = UserApplication(service)
    app.run()
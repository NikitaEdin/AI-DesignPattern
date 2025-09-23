class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection_string = "mongodb://localhost:27017"
        return cls._instance

    def get_data(self):
        return "Sample data from database"


if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(db1 is db2)
    print(db1.get_data())
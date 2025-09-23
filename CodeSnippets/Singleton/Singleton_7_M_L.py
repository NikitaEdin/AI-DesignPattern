class DatabaseConnection:
    __instance = None

    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection.__instance = self

    @staticmethod
    def get_connection():
        if DatabaseConnection.__instance is None:
            return DatabaseConnection()
        else:
            return DatabaseConnection.__instance

def main():
    connection1 = DatabaseConnection.get_connection()
    connection2 = DatabaseConnection.get_connection()
    print(f"Connection 1: {connection1}")
    print(f"Connection 2: {connection2}")
    print(f"Same instance?: {connection1 is connection2}")

if __name__ == "__main__":
    main()
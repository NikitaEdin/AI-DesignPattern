class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.connection = "database connected"

def main():
    mgr1 = DatabaseManager()
    mgr2 = DatabaseManager()
    print(mgr1 is mgr2)
    print(mgr1.connection)

if __name__ == "__main__":
    main()
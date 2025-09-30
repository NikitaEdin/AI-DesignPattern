class ApplicationManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config = {}
            self.users = []
            self._initialized = True
    
    def set_config(self, key, value):
        self.config[key] = value
    
    def get_config(self, key):
        return self.config.get(key)
    
    def add_user(self, username):
        if username not in self.users:
            self.users.append(username)
            return True
        return False
    
    def get_user_count(self):
        return len(self.users)

if __name__ == "__main__":
    manager1 = ApplicationManager()
    manager1.set_config("theme", "dark")
    manager1.add_user("alice")
    
    manager2 = ApplicationManager()
    manager2.set_config("language", "python")
    manager2.add_user("bob")
    
    print(manager1 is manager2)
    print(manager1.get_config("theme"))
    print(manager1.get_config("language"))
    print(manager1.get_user_count())
    print(manager2.get_user_count())
class ConfigHub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = {}
        return cls._instance

    def set(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db.get(key)

if __name__ == "__main__":
    a = ConfigHub()
    b = ConfigHub()
    a.set("mode", "prod")
    print(a is b)
    print(b.get("mode"))
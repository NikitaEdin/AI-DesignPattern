class GlobalConfig:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, 'settings'):
            self.settings = {}
    def set(self, key, value):
        self.settings[key] = value
    def get(self, key, default=None):
        return self.settings.get(key, default)

if __name__ == '__main__':
    a = GlobalConfig()
    b = GlobalConfig()
    a.set('mode', 'production')
    print(b.get('mode'))
    print(a is b)
    print(id(a), id(b))
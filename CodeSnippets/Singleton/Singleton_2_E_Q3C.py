class Configuration:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.data = {}

def main():
    config1 = Configuration()
    config2 = Configuration()
    
    print(config1 is config2)  # True
    
    config1.data['setting'] = 'value'
    print(config2.data['setting'])  # value

if __name__ == "__main__":
    main()
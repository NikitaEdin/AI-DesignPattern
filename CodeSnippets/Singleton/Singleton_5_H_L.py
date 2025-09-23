class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, data=None):
        self.data = data

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Singleton instance does not exist")
        return cls._instance
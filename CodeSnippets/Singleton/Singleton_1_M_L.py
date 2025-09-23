class Singleton:
    def __init__(self):
        if not hasattr(self.__class__, 'instance'):
            self.__class__.instance = self

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance
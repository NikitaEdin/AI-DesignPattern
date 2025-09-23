class MyClass:
    _instance = None

    def __init__(self):
        if MyClass._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MyClass._instance = self

    @classmethod
    def get_instance(cls):
        return cls._instance
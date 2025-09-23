class UniqueClass:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        print("UniqueClass initialized!")

class Main:
    @staticmethod
    def main():
        obj1 = UniqueClass()
        obj2 = UniqueClass()
        print(obj1 is obj2)  # Output: True

if __name__ == "__main__":
    Main.main()
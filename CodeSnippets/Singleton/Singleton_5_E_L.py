class MySingleton:
    def __init__(self):
        self._instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

def main():
    # create two instances of the singleton class
    a = MySingleton.instance()
    b = MySingleton.instance()

    # check if both instances are the same
    print(a is b)  # True

if __name__ == "__main__":
    main()
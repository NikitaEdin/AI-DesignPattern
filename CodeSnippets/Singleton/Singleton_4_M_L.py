class MySingleton:
    """
    A class that implements the Singleton design pattern.
    """

    _instance = None

    def __init__(self):
        if not MySingleton._instance:
            MySingleton._instance = self

    @staticmethod
    def get_instance():
        if not MySingleton._instance:
            return MySingleton()
        else:
            return MySingleton._instance

if __name__ == "__main__":
    # usage example
    instance1 = MySingleton.get_instance()
    instance2 = MySingleton.get_instance()
    print(id(instance1))  # prints the same id as instance2
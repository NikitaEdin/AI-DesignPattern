class MySingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if not MySingleton.__instance:
            MySingleton()
        return MySingleton.__instance

    def __init__(self):
        if MySingleton.__instance:
            raise Exception("This is a singleton class")
        else:
            MySingleton.__instance = self

class AnotherClass:
    def some_method(self):
        # Use the singleton instance here
        singleton_instance = MySingleton.get_instance()
        print(singleton_instance)

if __name__ == "__main__":
    # Test the singleton class
    another_class = AnotherClass()
    another_class.some_method()
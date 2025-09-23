class MySingleton:
    _instance = None

    def __init__(self):
        if MySingleton._instance is not None:
            raise RuntimeError("This class is a singleton!")
        else:
            MySingleton._instance = self

    @staticmethod
    def get_instance():
        if MySingleton._instance is None:
            MySingleton()
        return MySingleton._instance

class AnotherClass:
    def __init__(self):
        self.my_singleton = MySingleton.get_instance()

if __name__ == "__main__":
    another_class1 = AnotherClass()
    another_class2 = AnotherClass()
    print(another_class1.my_singleton is another_class2.my_singleton) # True
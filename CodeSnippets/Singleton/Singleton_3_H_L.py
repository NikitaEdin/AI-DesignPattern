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
            return MySingleton()
        else:
            return MySingleton._instance

    def do_something(self):
        print("I'm doing something!")
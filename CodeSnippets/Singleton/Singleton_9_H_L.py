class MySingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if not MySingleton.__instance:
            MySingleton()
        return MySingleton.__instance

    def __init__(self):
        if MySingleton.__instance:
            raise Exception("This class is a singleton!")
        else:
            MySingleton.__instance = self
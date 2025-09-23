class Logger:
    __instance = None

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("Logger is a singleton class.")
        else:
            Logger.__instance = self

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            return Logger()
        else:
            return Logger.__instance
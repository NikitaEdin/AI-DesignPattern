class Logger:
    def __init__(self):
        self._logger = logging.getLogger()
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.setLevel(logging.INFO)

    def log(self, message):
        self._logger.info(message)

class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance
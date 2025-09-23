class Logger:
    """
    A simple logger class that implements the Singleton design pattern.
    It ensures that there is only one instance of the class at any given time.
    """
    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise RuntimeError("Cannot instantiate a second instance of Logger")
        else:
            Logger._instance = self

    @classmethod
    def get_instance(cls) -> "Logger":
        """
        Returns the singleton instance of the Logger class.
        """
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def log(self, message: str):
        """
        Logs a message to the console.
        """
        print(message)

if __name__ == "__main__":
    # Create an instance of the logger
    logger = Logger.get_instance()

    # Use the logger to log some messages
    logger.log("Hello, world!")
    logger.log("This is a message")
    logger.log("Another message")

    # Get another reference to the logger
    logger2 = Logger.get_instance()

    # Both references should be the same instance
    assert logger == logger2
class Logger:
    def log(self, level, message):
        pass

class ConsolePrinter:
    def print_message(self, message):
        print(message)

class ConsoleLogger:
    def __init__(self, printer):
        self.printer = printer

    def log(self, level, message):
        self.printer.print_message(f"[{level}] {message}")

if __name__ == "__main__":
    printer = ConsolePrinter()
    logger = ConsoleLogger(printer)
    logger.log("INFO", "Hello World")
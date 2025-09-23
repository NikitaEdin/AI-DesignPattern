from abc import ABC, abstractmethod

class PrinterInterface(ABC):
    @abstractmethod
    def modern_print(self, message):
        pass

class OldPrinter:
    def old_print(self, text):
        return f"Old: {text}"

class PrinterBridge(PrinterInterface):
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def modern_print(self, message):
        return self.old_printer.old_print(message)

class ModernPrinter(PrinterInterface):
    def modern_print(self, message):
        return f"Modern: {message}"

class Application:
    def __init__(self, printer):
        self.printer = printer
    
    def execute(self, text):
        return self.printer.modern_print(text)

if __name__ == "__main__":
    old_printer = OldPrinter()
    bridge = PrinterBridge(old_printer)
    app = Application(bridge)
    print(app.execute("Hello World"))
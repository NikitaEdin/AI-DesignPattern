from abc import ABC, abstractmethod

class Printer(ABC):
    @abstractmethod
    def print_document(self, text):
        pass

class OldPrinter:
    def old_print(self, content):
        print(f"Legacy output: {content}")

class PrinterWrapper(Printer):
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print_document(self, text):
        self.old_printer.old_print(text)

class ModernPrinter(Printer):
    def print_document(self, text):
        print(f"Modern output: {text}")

if __name__ == "__main__":
    legacy = OldPrinter()
    wrapped_printer = PrinterWrapper(legacy)
    modern = ModernPrinter()
    
    printers = [wrapped_printer, modern]
    for printer in printers:
        printer.print_document("Hello World")
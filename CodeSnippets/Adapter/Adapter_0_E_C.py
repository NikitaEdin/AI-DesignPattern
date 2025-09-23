class OldPrinter:
    def old_print(self, text):
        return f"Old format: {text}"

class ModernPrinter:
    def print_message(self, message):
        return f"Modern format: {message}"

class PrinterBridge:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print_message(self, message):
        return self.old_printer.old_print(message)

def use_modern_printer(printer):
    return printer.print_message("Hello World")

if __name__ == "__main__":
    old = OldPrinter()
    modern = ModernPrinter()
    bridge = PrinterBridge(old)
    
    print(use_modern_printer(modern))
    print(use_modern_printer(bridge))
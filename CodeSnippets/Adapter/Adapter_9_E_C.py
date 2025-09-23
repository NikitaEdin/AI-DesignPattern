class OldPrinter:
    def old_print(self, text):
        return f"Old: {text}"

class NewPrinter:
    def print_message(self, message):
        return f"New: {message}"

class PrinterBridge:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print_message(self, message):
        return self.old_printer.old_print(message)

if __name__ == "__main__":
    old = OldPrinter()
    new = NewPrinter()
    bridge = PrinterBridge(old)
    
    print(new.print_message("Hello"))
    print(bridge.print_message("Hello"))
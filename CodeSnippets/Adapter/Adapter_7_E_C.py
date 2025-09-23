class OldPrinter:
    def old_print(self, text):
        return f"Old printer: {text}"

class NewPrinter:
    def print_document(self, content):
        return f"New printer: {content}"

class PrinterBridge:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print_document(self, content):
        return self.old_printer.old_print(content)

def use_printer(printer, text):
    return printer.print_document(text)

if __name__ == "__main__":
    old = OldPrinter()
    new = NewPrinter()
    bridge = PrinterBridge(old)
    
    print(use_printer(new, "Hello World"))
    print(use_printer(bridge, "Hello World"))
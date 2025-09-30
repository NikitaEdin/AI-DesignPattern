class OldPrinter:
    def old_print(self, text):
        return f"Legacy: {text}"

class NewPrinter:
    def print(self, text):
        return f"Modern: {text}"

class PrinterWrapper:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def print(self, text):
        return self.old_printer.old_print(text)

if __name__ == "__main__":
    legacy = OldPrinter()
    wrapper = PrinterWrapper(legacy)
    print(wrapper.print("Hello"))
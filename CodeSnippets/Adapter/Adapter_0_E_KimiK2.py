class OldPrinter:
    def old_print(self, text):
        return f"Old: {text}"

class NewPrinter:
    def new_print(self, text):
        return f"New: {text}"

class CompatiblePrinter:
    def __init__(self, printer):
        self.printer = printer
    
    def print(self, text):
        if hasattr(self.printer, 'new_print'):
            return self.printer.new_print(text)
        else:
            return self.printer.old_print(text)

if __name__ == "__main__":
    old = OldPrinter()
    new = NewPrinter()
    
    compatible_old = CompatiblePrinter(old)
    compatible_new = CompatiblePrinter(new)
    
    print(compatible_old.print("Hello"))
    print(compatible_new.print("World"))
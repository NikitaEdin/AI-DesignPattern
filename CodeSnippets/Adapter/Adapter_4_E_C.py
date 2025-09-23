class OldPrinter:
    def old_print(self, text):
        return f"OLD: {text}"

class NewSystem:
    def __init__(self, printer):
        self.printer = printer
    
    def print_message(self, message):
        return self.printer.modern_print(message)

class Bridge:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def modern_print(self, text):
        return self.old_printer.old_print(text)

if __name__ == "__main__":
    old_printer = OldPrinter()
    bridge = Bridge(old_printer)
    new_system = NewSystem(bridge)
    
    result = new_system.print_message("Hello World")
    print(result)
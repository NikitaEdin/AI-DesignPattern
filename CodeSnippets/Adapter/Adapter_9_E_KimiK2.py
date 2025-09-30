class OldPrinter:
    def old_print(self, text):
        return f"Legacy: {text}"

class NewSystem:
    def display(self, content):
        return f"Displaying: {content}"

class Bridge:
    def __init__(self, old_printer):
        self.old_printer = old_printer
    
    def display(self, content):
        return self.old_printer.old_print(content)

if __name__ == "__main__":
    legacy = OldPrinter()
    bridge = Bridge(legacy)
    result = bridge.display("Hello World")
    print(result)
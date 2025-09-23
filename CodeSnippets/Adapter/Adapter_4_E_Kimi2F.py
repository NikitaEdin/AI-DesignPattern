class OldPrinter:
    def old_print(self, text):
        return f"Legacy print: {text}"

class NewPrinter:
    def print(self, text):
        return f"Modern print: {text}"

class PrinterWrapper:
    def __init__(self, old_device):
        self.old_device = old_device
    
    def print(self, text):
        return self.old_device.old_print(text)

if __name__ == "__main__":
    legacy = OldPrinter()
    wrapper = PrinterWrapper(legacy)
    print(wrapper.print("Hello"))
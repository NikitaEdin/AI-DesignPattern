class PrinterInterface:
    def print(self, text):
        raise NotImplementedError

class OldPrinter:
    def old_print(self, data):
        print("OldPrinter:", data.decode())

class NewPrinter(PrinterInterface):
    def print(self, text):
        print("NewPrinter:", text)

class PrinterWrapper(PrinterInterface):
    def __init__(self, old):
        self._old = old
    def print(self, text):
        self._old.old_print(text.encode())

if __name__ == "__main__":
    new = NewPrinter()
    old = OldPrinter()
    devices = [new, PrinterWrapper(old)]
    for device in devices:
        device.print("Hello World")
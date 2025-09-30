class Printer:
    def print(self, data): pass

class ConsolePrinter(Printer):
    def print(self, data): print(data)

class ReversePrinter(Printer):
    def print(self, data): print(data[::-1])

class App:
    def __init__(self): self.printer = ConsolePrinter()
    def set_printer(self, printer): self.printer = printer
    def run(self, data): self.printer.print(data)

if __name__ == "__main__":
    app = App()
    app.run("hello")
    app.set_printer(ReversePrinter())
    app.run("hello")
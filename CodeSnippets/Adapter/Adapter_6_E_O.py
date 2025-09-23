class Target:
    def perform_action(self, data):
        raise NotImplementedError

class LegacyPrinter:
    def do_work(self, text):
        return f"legacy output -> {text[::-1]}"

class PrinterWrapper(Target):
    def __init__(self, legacy):
        self.legacy = legacy
    def perform_action(self, data):
        return self.legacy.do_work(data)

if __name__ == "__main__":
    legacy = LegacyPrinter()
    service: Target = PrinterWrapper(legacy)
    print(service.perform_action("Hello World"))
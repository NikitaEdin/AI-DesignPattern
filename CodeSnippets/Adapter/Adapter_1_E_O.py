class ExpectedService:
    def send(self, message):
        raise NotImplementedError

class LegacyPrinter:
    def print_long(self, message):
        print(f"[LEGACY] {message.upper()}")

class WrapperService(ExpectedService):
    def __init__(self, legacy):
        self.legacy = legacy
    def send(self, message):
        self.legacy.print_long(message)

class Client:
    def __init__(self, service):
        self.service = service
    def run(self):
        self.service.send("Hello from client")

if __name__ == "__main__":
    legacy = LegacyPrinter()
    service = WrapperService(legacy)
    Client(service).run()
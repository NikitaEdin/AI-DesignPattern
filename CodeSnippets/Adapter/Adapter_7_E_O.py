class ServiceInterface:
    def perform(self):
        raise NotImplementedError

class ConcreteService(ServiceInterface):
    def perform(self):
        return "Result from concrete service"

class LegacyService:
    def legacy_call(self, value):
        return f"Legacy processed {value}"

class ServiceBridge(ServiceInterface):
    def __init__(self, legacy):
        self.legacy = legacy
    def perform(self):
        data = "input"
        return self.legacy.legacy_call(data)

def main():
    services = [ConcreteService(), ServiceBridge(LegacyService())]
    for s in services:
        print(s.perform())

if __name__ == "__main__":
    main()